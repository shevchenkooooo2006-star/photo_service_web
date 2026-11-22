from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный пользователь с ролью (клиент, фотограф, админ)."""

    class Role(models.TextChoices):
        CLIENT = "client", "Клиент"
        PHOTOGRAPHER = "photographer", "Фотограф"
        ADMIN = "admin", "Администратор"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name="Роль",
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Client(models.Model):
    """Профиль клиента — заказчика фотосессии."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="client_profile",
        verbose_name="Пользователь",
    )
    name = models.CharField(max_length=120, verbose_name="Имя")
    email = models.EmailField(unique=True, verbose_name="Email")

    def __str__(self):
        return f"{self.name} <{self.email}>"
