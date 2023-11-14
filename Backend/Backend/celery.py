from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set an environment variable so that Celery knows where the settings.py file of your Django project is located.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

app = Celery('Backend')

# Load configuration from settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically find and register tasks in tasks.py files in your Django applications.
app.autodiscover_tasks()

# Add configuration for periodic tasks
app.conf.beat_schedule = {
    'run-every-day-at-midnight': {
        'task': 'quizzes.tasks.check_user_quiz_schedule',
        'schedule': crontab(hour=0, minute=0),  # Every day at midnight
    },
}
