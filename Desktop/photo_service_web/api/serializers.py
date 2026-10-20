from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model

from users.models import Client
from photographers.models import Photographer
from locations.models import Location
from bookings.models import Booking

User = get_user_model()


class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ["id", "name", "rating", "hourly_rate", "min_hours"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "rent_price"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "email"]


class BookingSerializer(serializers.ModelSerializer):
    photographer_detail = PhotographerSerializer(source="photographer", read_only=True)
    location_detail = LocationSerializer(source="location", read_only=True)
    client_detail = ClientSerializer(source="client", read_only=True)
    total_cost = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id", "photographer", "photographer_detail", 
            "location", "location_detail", "client", "client_detail",
            "shoot_date", "hours", "need_makeup", "is_cancelled", "total_cost", "status"
        ]
        read_only_fields = ["is_cancelled"]

    def get_total_cost(self, obj):
        return float(obj.calculate_total_cost())

    def get_status(self, obj):
        return obj.get_status()

    def validate(self, attrs):
        """Проверка доступности (запрет дублей)."""
        # Получаем данные из запроса
        photographer = attrs.get('photographer')
        location = attrs.get('location')
        shoot_date = attrs.get('shoot_date')

        # Проверяем, есть ли уже активная бронь у этого фотографа на эту дату
        if Booking.objects.filter(
            photographer=photographer, shoot_date=shoot_date, is_cancelled=False
        ).exists():
            raise serializers.ValidationError({"photographer": "Фотограф уже занят на эту дату."})

        # Проверяем локацию
        if Booking.objects.filter(
            location=location, shoot_date=shoot_date, is_cancelled=False
        ).exists():
            raise serializers.ValidationError({"location": "Локация уже занята на эту дату."})

        return attrs


# Тот самый сериализатор, которого не хватало
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)