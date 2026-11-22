from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=150)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.rent_price} руб./ч)"
