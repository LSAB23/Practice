from django import template

register = template.Library()

@register.filter
def get_filter(obj,ques_id):
    return obj.answers_set.filter(ques_id=ques_id)