from django import template

register = template.Library()

@register.filter(name='split')
def split(mystring, separator: str):
    """Split path string by delimiter"""
    return str(mystring).split(separator)


@register.filter(name='is_student')
def is_student(user):
    return hasattr(user, 'student')

@register.filter(name='is_teacher')
def is_student(user):
    return hasattr(user, 'teacher')