from django.db import models
from django.contrib.auth.models import User




class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) # type: ignore
    quiz_id = models.CharField(unique=True, primary_key=True,max_length=7, editable=False)
    quiz_name = models.CharField(max_length=255, unique=True)
    date_created = models.DateField(auto_now_add=True, editable=False)

class Questions(models.Model):
    quiz_id = models.ForeignKey(Quiz, editable=False, on_delete=models.CASCADE)
    ques_id = models.CharField(unique=True,max_length=7, primary_key=True, editable=False)
    ques = models.CharField(max_length=1000)
    ques_image = models.ImageField(default=None,upload_to='uploads/question_images')
    ques_date = models.DateField(auto_now_add=True, editable=False)

class Answers(models.Model):
    quiz_id = models.ForeignKey(Quiz, editable=False, on_delete=models.CASCADE)
    ques_id = models.ForeignKey(Questions, editable=False, on_delete=models.CASCADE)
    ans_id = models.CharField(unique=True, primary_key=True,editable=False, max_length=7)
    ans = models.CharField(max_length=1000)
    ans_image = models.ImageField(default=None, upload_to='uploads/answer_images')
    ans_correct = models.BooleanField(default=False)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.CharField(max_length=1000000)
    wrong = models.CharField(max_length=1000000000000000000)
    correct = models.CharField(max_length=1000000000000000000)
    wrong_len = models.IntegerField()
    correct_len = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)