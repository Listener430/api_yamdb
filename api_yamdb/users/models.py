from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class RoleChoices:
        USER = "user"
        ADMIN = "admin"
        MODERATOR = "moderator"
        choices = [
            (USER, "user"),
            (ADMIN, "admin"),
            (MODERATOR, "moderator"),
        ]

    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=30,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )

    @property
    def is_admin(self):
        return self.role == self.RoleChoices.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.RoleChoices.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["id"]
