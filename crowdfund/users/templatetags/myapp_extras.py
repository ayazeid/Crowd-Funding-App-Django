from django import template

register = template.Library()

@register.filter(is_safe=True)
def sum_total_count(value):
    sum = 0
    for v in value:
        sum += v.amount
    return sum


@register.filter(is_safe=True)
def sum_total_rate(value):
    sum = 0
    for v in value:
        sum += v.rating
    return sum