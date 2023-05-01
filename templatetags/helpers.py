from django import template
register = template.Library()

@register.simple_tag
def get_subject(subjects,subject_code):
    return subjects.filter(subject_code=subject_code).first()