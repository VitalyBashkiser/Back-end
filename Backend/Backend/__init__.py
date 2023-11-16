from __future__ import absolute_import, unicode_literals

# Overrides the default Django settings module for use with Celery.
from .celery import app as celery_app

__all__ = ('celery_app',)