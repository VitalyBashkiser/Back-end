# Generated by Django 4.2.6 on 2023-11-06 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('UN', 'Unread'), ('RE', 'Read')], default='UN', max_length=2)),
                ('text', models.TextField()),
            ],
        ),
    ]