from django.db import models
from django.contrib.auth.models import User
from main.models import TimeStampedModel


class Company(TimeStampedModel):
    name = models.CharField(max_length=150)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    is_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
