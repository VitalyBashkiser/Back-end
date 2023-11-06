from django.db import models


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

    def mark_as_read(self):
        self.status = self.Status.READ
        self.save()
