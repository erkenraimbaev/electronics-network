from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class UserRole(models.TextChoices):
    USER = "user"
    ADMIN = "admin"


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=15, verbose_name="телефон", **NULLABLE)
    role = models.CharField(
        max_length=30, verbose_name="role", choices=UserRole.choices, default="user"
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
