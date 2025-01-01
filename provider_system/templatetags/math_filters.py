from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return int(float(value) * float(arg))