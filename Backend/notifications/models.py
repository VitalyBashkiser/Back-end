from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    class Status(models.TextChoices):
        UNREAD = 'UN', 'Unread'
        READ = 'RE', 'Read'

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.UNREAD,
    )
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def mark_as_read(self):
        self.status = self.Status.READ
        self.save()
