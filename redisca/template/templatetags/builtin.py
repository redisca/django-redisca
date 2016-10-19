from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def assign(context, **kwargs):
    """
    Usage:
    {% assign hello="Hello Django" %}
    """

    for key, value in kwargs.items():
        context[key] = value
    return ''


@register.filter
def get(content, key):
    """
    Usage:
    {% object|get:key|get:key %}
    """
    if isinstance(content, dict):
        return content.get(key, '')
    if isinstance(content, object):
        return getattr(content, key, '')
    return ''


@register.simple_tag()
def call(fn, *args, **kwargs):
    """
    Usage:
    {% call object.method *args **kwargs %}
    Callable function should be decorated with
    redisca.template.decorators.template_func.
    """
    if callable(fn):
        return fn(*args, **kwargs)
    return fn
