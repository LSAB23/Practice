from django import template
import ast
from django.template.loader import render_to_string

register = template.Library()

@register.filter
def get_filter(obj,ques_id):
    return obj.answers_set.filter(ques_id=ques_id)

@register.filter
def check_html(answer):
    contexts = ast.literal_eval(answer.correct)
    contexts.append(ast.literal_eval(answer.wrong))
    template = []
    for i in contexts:
        if type(i) == type(list()):
            for context in i:
                template.append(render_to_string('check.html', context))
        else:
            template.append(render_to_string('check.html', i))

    return render_to_string('results.html', {'lst_template':template})
 
