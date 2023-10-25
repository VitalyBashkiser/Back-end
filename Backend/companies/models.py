from django.db import models
from django.contrib.auth.models import User
from main.models import TimeStampedModel
from .enums import RequestStatus


class Company(TimeStampedModel):
    name = models.CharField(max_length=150)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_companies')
    is_visible = models.BooleanField(default=True)
    members = models.ManyToManyField(User, related_name='companies')

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Invitation(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"Invitation for {self.user.username} to {self.company.name}"


class Request(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    STATUS_CHOICES = [(status.value, status.name) for status in RequestStatus]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Request from {self.user.username} to {self.company.name}"

