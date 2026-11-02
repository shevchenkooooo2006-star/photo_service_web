from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный пользователь с ролью."""

    class Role(models.TextChoices):
        CLIENT = "client", "Клиент"
        PHOTOGRAPHER = "photographer", "Фотограф"
        ADMIN = "admin", "Администратор"

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.CLIENT
    )


class Client(models.Model):
    """Профиль клиента."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"