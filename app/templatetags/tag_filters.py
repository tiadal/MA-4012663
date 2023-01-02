from django import template

register = template.Library()

@register.filter(name='end_table')
def end_table(value):
    value = value.replace('{"answer": "', 'value: ')
    value = value.replace('"}', '')
    return value