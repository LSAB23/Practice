# Generated by Django 5.1.3 on 2024-11-30 23:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.CharField(editable=False, max_length=7, primary_key=True, serialize=False, unique=True)),
                ('quiz_name', models.CharField(max_length=255, unique=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('ques_id', models.CharField(editable=False, max_length=7, primary_key=True, serialize=False, unique=True)),
                ('ques', models.CharField(max_length=1000)),
                ('ques_image', models.ImageField(default=None, upload_to='uploads/question_images')),
                ('ques_date', models.DateField(auto_now_add=True)),
                ('quiz_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='studybud.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('ans_id', models.CharField(editable=False, max_length=7, primary_key=True, serialize=False, unique=True)),
                ('ans', models.CharField(max_length=1000)),
                ('ans_image', models.ImageField(default=None, upload_to='uploads/answer_images')),
                ('ans_correct', models.BooleanField(default=False)),
                ('ques_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='studybud.questions')),
                ('quiz_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='studybud.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=1000000)),
                ('wrong', models.CharField(max_length=1000000000000000000)),
                ('correct', models.CharField(max_length=1000000000000000000)),
                ('wrong_len', models.IntegerField()),
                ('correct_len', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studybud.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]