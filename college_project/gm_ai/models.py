from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    passport_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    permanent_address = models.TextField()

    def __str__(self):
        return self.username
