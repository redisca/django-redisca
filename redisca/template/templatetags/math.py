from django.template import Library

register = Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def division(value, arg):
    return value / arg
