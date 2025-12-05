from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        FARMER = "FARMER", "Farmer"
        OFFICER = "OFFICER", "Extension Officer"
        ADMIN = "ADMIN", "Admin"
        SACCO_BANK = "SACCO_BANK", "SACCO/Bank"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.FARMER)
    
    # Add common profile fields here or link to a Profile model
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser:
            self.role = self.Role.ADMIN
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
