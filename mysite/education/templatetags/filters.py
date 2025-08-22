from django import template

register = template.Library()

@register.filter(name='split')
def split(mystring, separator: str):
    """Split path string by delimiter"""
    return str(mystring).split(separator)