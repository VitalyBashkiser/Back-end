from django.db import models
from django.utils import timezone
from .utils import logger, some_function
from django.contrib.auth.models import AbstractUser, Group, Permission

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AuthGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser, TimeStampedModel):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='savage_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='global_permissions'
    )