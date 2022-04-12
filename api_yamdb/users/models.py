from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = "user", "user"
        MODERATOR = "moderator", "moderator"
        ADMIN = "admin", "admin"

    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=30,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )
    confirmation_code = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username
