from decimal import Decimal

from django.db import models

from photographers.models import Photographer
from locations.models import Location
from users.models import Client


class Booking(models.Model):
    """Бронирование фотосессии."""

    MAKEUP_PRICE = Decimal("2500.00")

    photographer = models.ForeignKey(
        Photographer,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Фотограф",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Локация",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Клиент",
    )
    shoot_date = models.DateField(verbose_name="Дата съёмки")
    hours = models.PositiveIntegerField(verbose_name="Длительность, ч")
    need_makeup = models.BooleanField(
        default=False, verbose_name="Нужен визажист"
    )
    is_cancelled = models.BooleanField(default=False)

    def __str__(self) -> str:
        state = "ОТМЕНЕНО" if self.is_cancelled else "активно"
        return (
            f"[{self.pk}] {self.client.name} → {self.photographer.name} "
            f"({state})"
        )

    def calculate_base_cost(self) -> Decimal:
        """Базовая стоимость: работа фотографа + аренда локации."""
        return (
            Decimal(self.hours) * self.photographer.hourly_rate
            + Decimal(self.hours) * self.location.rent_price
        )

    def calculate_total_cost(self) -> Decimal:
        """Итоговая стоимость с учётом дополнительных услуг."""
        base = self.calculate_base_cost()
        if self.need_makeup:
            return base + self.MAKEUP_PRICE
        return base

    def cancel(self) -> None:
        """Отменить бронирование (не удаляя объект)."""
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])
        
    def get_status(self) -> str:
        """Текстовый статус бронирования."""
        if self.is_cancelled:
            return "Бронирование отменено."
        return "Бронирование подтверждено."