# Generated by Django 4.2.6 on 2023-11-06 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_merge_20231031_1342'),
        ('quizzes', '0006_alter_testresult_question_alter_testresult_quiz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.company'),
        ),
    ]
