from django.db import models


class Location(models.Model):
    """Локация для проведения фотосессии."""

    name = models.CharField(max_length=150, verbose_name="Название")
    rent_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Аренда, руб./ч"
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.rent_price} руб./ч)"