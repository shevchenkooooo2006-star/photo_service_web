from django.db import models


class Photographer(models.Model):
    """Фотограф."""

    name = models.CharField(max_length=120, verbose_name="Имя")
    rating = models.FloatField(default=5.0, verbose_name="Рейтинг")
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ставка, руб./ч"
    )
    min_hours = models.PositiveIntegerField(
        default=1, verbose_name="Минимум часов"
    )

    def __str__(self) -> str:
        return (
            f"{self.name} (рейтинг {self.rating}, "
            f"{self.hourly_rate} руб./ч)"
        )

    def is_suitable_for(self, hours: int) -> bool:
        """Проверить, подходит ли фотограф по длительности съёмки."""
        return hours >= self.min_hours