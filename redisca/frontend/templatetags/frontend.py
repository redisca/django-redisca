import os
import re

from django.template import Library
from django.utils.html import mark_safe
from django.conf import settings

from ..html import parse_attrs, tags


wrapper_regex = re.compile(r'<svg([^>]*)>(.*)<\/svg>', re.I)
space_regex = re.compile(r'\s+')
register = Library()
svg_cache = {}


@register.simple_tag
def svg_icon(svg_path):
    if svg_path in svg_cache:
        return mark_safe(svg_cache[svg_path])

    filepath = os.path.join(settings.FRONTEND_DIRS['svg'], svg_path)

    try:
        svg = optimize_svg(open(filepath, 'r').read())
        svg = wrap_comment(svg_path, svg)
        svg_cache[svg_path] = svg
        return mark_safe(svg)
    except (FileNotFoundError, IsADirectoryError):
        relpath = os.path.relpath(filepath, settings.BASE_DIR)
        return mark_safe('<!-- ERROR: svg icon not found in {} -->'.format(relpath))


def optimize_svg(content):
    if '\n' in content:
        content = content.replace('\n', '').replace('\r', '')
        content = space_regex.sub(' ', content)
        content = content.replace('> <', '><')

    match = wrapper_regex.search(content)

    if not match:
        return content

    attrs = parse_attrs(match.group(1))
    attrs.pop('id', None)

    inner = match.group(2)
    return tags.svg(inner, attrs)


def wrap_comment(name, content):
    prefix = '<!-- {} -->'.format(name)
    suffix = '<!-- /{} -->'.format(name)
    return prefix + content + suffix
