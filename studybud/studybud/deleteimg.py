from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete
from .models import Answers, Questions


@receiver([pre_delete])
def delete_image(sender, instance, **kwargs):
    name = instance.__class__.__name__
    try:
        if name == 'Answers':
            instance.ans_image.delete()
        elif name == 'Questions':
            instance.ques_image.delete()
    except:
        raise "don't forget to add the errors to a logfile"