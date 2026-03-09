from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending')
    ]

