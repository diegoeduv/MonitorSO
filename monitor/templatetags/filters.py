from django import template

register = template.Library()

@register.filter
def to_gb(value):
    try:
        gb = value / (1024 ** 3)
        return f"{gb:.2f} GB"
    except:
        return value
