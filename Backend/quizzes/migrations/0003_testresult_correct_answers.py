# Generated by Django 4.2.6 on 2023-10-25 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_testresult_lasttesttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='correct_answers',
            field=models.IntegerField(default=0),
        ),
    ]
