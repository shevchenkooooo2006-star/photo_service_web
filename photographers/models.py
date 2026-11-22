from django.db import models


class Photographer(models.Model):
    name = models.CharField(max_length=120)
    rating = models.FloatField(default=5.0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    min_hours = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} (рейтинг {self.rating})"

    def is_suitable_for(self, hours: int) -> bool:
        return hours >= self.min_hours
