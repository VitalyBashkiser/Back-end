from django.db import models
from main.models import TimeStampedModel

class Company(TimeStampedModel):
    name = models.CharField(max_length=150)
    description = models.TextField()
    owner = models.ForeignKey('main.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
