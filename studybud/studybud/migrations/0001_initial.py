# Generated by Django 5.1.1 on 2024-09-28 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.CharField(editable=False, max_length=5, primary_key=True, serialize=False, unique=True)),
                ('quiz_name', models.CharField(max_length=255)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('ques_id', models.CharField(editable=False, max_length=5, primary_key=True, serialize=False, unique=True)),
                ('ques', models.CharField(max_length=1000)),
                ('ques_image', models.ImageField(default=None, upload_to='')),
                ('ques_date', models.DateField(auto_now_add=True)),
                ('quiz_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='studybud.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('ans_id', models.CharField(editable=False, max_length=5, primary_key=True, serialize=False, unique=True)),
                ('ans', models.CharField(max_length=1000)),
                ('ans_image', models.ImageField(default=None, upload_to='')),
                ('ans_correct', models.BooleanField(default=False)),
                ('ques_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='studybud.questions')),
                ('quiz_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='studybud.quiz')),
            ],
        ),
    ]
