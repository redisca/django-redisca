from django.template import Library
register = Library()


@register.filter
def to_int(value):
    return int(value)


@register.filter
def to_str(value):
    return str(value)


@register.filter
def to_bool(value):
    if type(value) == str and value.isdigit():
        value = int(value)
    return bool(value)


@register.filter(name='type')
def type_(value):
    return type(value).__name__
