# Generated by Django 4.2.6 on 2023-10-29 16:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_question_answers_ref_alter_answer_answer_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='date_passed',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(),
        ),
    ]
