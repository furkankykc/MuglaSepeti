from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def modulo(num, val):
    return num % val


@register.filter
def subtract(num, val):
    return int(num) - val


@register.filter(is_safe=True)
@stringfilter
def ljusts(value, arg):
    """Left-align the value in a field of a given width."""
    return value.ljust(int(5 - int(arg)))


@register.filter(is_safe=True)
@stringfilter
def hiddenowner(value):
    return value[0] + '*' * (len(value) - 1)


@register.filter(is_safe=True)
@stringfilter
def quote(value):
    return "".join(value.split("-")[::-1])


@register.filter(is_safe=True)
@stringfilter
def lquote(value):
    return "".join(value.split("-")[-1])
