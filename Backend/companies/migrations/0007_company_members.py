# Generated by Django 4.2.6 on 2023-10-23 19:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0006_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='members',
            field=models.ManyToManyField(related_name='member_of_companies', to=settings.AUTH_USER_MODEL),
        ),
    ]