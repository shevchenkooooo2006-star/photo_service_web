import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from photographers.models import Photographer
from locations.models import Location
from users.models import Client

User = get_user_model()


@pytest.fixture
def auth_client(db):
    """Фикстура: создает пользователя, клиента и авторизованный клиент API."""
    user = User.objects.create_user(username="test", password="123456")
    client_obj = Client.objects.create(name="Иван", email="ivan@example.com", user=user)
    api = APIClient()
    api.force_authenticate(user=user) # Авторизуем клиент насильно (без JWT токена, для скорости)
    return api, user, client_obj


@pytest.mark.django_db
def test_create_booking(auth_client):
    """Проверяем успешное создание бронирования и расчет стоимости."""
    api, user, client_obj = auth_client
    ph = Photographer.objects.create(name="Анна", rating=4.8, hourly_rate=3500, min_hours=2)
    loc = Location.objects.create(name="Студия", rent_price=1500)
    
    # Дата на 5 дней вперед (чтобы не было ошибки "дата в прошлом")
    future_date = str(date.today() + timedelta(days=5))

    response = api.post("/api/bookings/", {
        "photographer": ph.id,
        "location": loc.id,
        "client": client_obj.id,
        "shoot_date": future_date,
        "hours": 3,
        "need_makeup": True,
    })
    
    assert response.status_code == 201 # 201 = Created
    # Проверяем расчет стоимости: 3 часа * 3500 + 3 часа * 1500 + 2500 (визажист) = 17500
    assert float(response.json()["total_cost"]) == 17500.0


@pytest.mark.django_db
def test_duplicate_booking_forbidden(auth_client):
    """Проверяем бизнес-правило: нельзя забронировать одного фотографа на одну дату дважды."""
    api, user, client_obj = auth_client
    ph = Photographer.objects.create(name="Анна", rating=4.8, hourly_rate=3500, min_hours=2)
    loc = Location.objects.create(name="Студия", rent_price=1500)
    future_date = str(date.today() + timedelta(days=5))

    payload = {
        "photographer": ph.id,
        "location": loc.id,
        "client": client_obj.id,
        "shoot_date": future_date,
        "hours": 3,
        "need_makeup": False,
    }
    
    # Первое бронирование создается успешно
    response1 = api.post("/api/bookings/", payload)
    assert response1.status_code == 201
    
    # Второе на ту же дату и того же фотографа - должно вернуть ошибку 400
    response2 = api.post("/api/bookings/", payload)
    assert response2.status_code == 400