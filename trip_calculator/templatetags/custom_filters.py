from django import template

register = template.Library()

@register.filter(name='startswith')
def startswith(value, prefix):
    return str(value).startswith(str(prefix))