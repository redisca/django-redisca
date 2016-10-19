from collections import OrderedDict

SINGLE_TAGS = ('input', 'link', 'img', 'br')


def render_tag(tag, content=None, attrs={}, _single=False, _xhtml=False):
    attrs = render_attrs(attrs)

    buf = []
    buf.append('<')
    buf.append(tag)

    if attrs:
        buf.append(' ')
        buf.append(attrs)

    if _xhtml and (_single and not content):
        buf.append(' />')
    else:
        buf.append('>')

    if content:
        buf.append(content)

    if content or not _single:
        buf.append('</{}>'.format(tag))

    return ''.join(buf)


def render_attrs(attrs, xhtml=False):
    result = []
    is_true = {'true'}
    is_false = {'false', 'none', 'null'}

    for key, value in attrs.items():
        key = key.strip('_').replace('_', '-')

        if type(value) == bool:
            if value:
                if xhtml:
                    result.append('{}="{}"'.format(key, key))
                else:
                    result.append(key)
        else:
            if type(value) != str:
                value = str(value)
            if value.lower() in is_true:
                if xhtml:
                    result.append('{}="{}"'.format(key, key))
                else:
                    result.append(key)
            elif value.lower() not in is_false:
                result.append('{}="{}"'.format(key, value))

    return ' '.join(result)


def parse_attrs(atts_str, order=True):
    attrs = OrderedDict() if order else {}

    buffer = StringBuffer()
    in_value = False
    attr_name = ''

    def fix_attr_name(attr_name):
        return attr_name.replace('-', '_')

    for char in atts_str:
        if char == ' ' and not in_value:
            if buffer:
                attr_name = str(buffer)
                attrs[fix_attr_name(attr_name)] = True
                buffer = StringBuffer()
            continue

        if char == '=':
            if not in_value:
                attr_name = str(buffer)
                buffer = StringBuffer()
            continue

        if char == '"':
            if in_value:
                attrs[fix_attr_name(attr_name)] = str(buffer)
                buffer = StringBuffer()
                in_value = False
            else:
                in_value = True
            continue

        buffer += char

    if buffer and not in_value:
        attr_name = str(buffer)
        attrs[fix_attr_name(attr_name)] = True

    return attrs


class HtmlTags:
    def __init__(self, xhtml=False):
        self.tags_preset = {tag: {'_single': True} for tag in SINGLE_TAGS}
        self.xhtml = xhtml

    def __getattr__(self, tag_name):
        def wrapper(content=None, attrs={}):
            kwargs = self.tags_preset.get(tag_name, {})
            return render_tag(tag_name, content, attrs, _xhtml=self.xhtml, **kwargs)
        return wrapper


class StringBuffer(list):
    def __str__(self):
        return ''.join(self)


tags = HtmlTags()
