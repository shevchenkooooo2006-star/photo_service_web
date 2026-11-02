import pytest
from rest_framework.test import APIClient
from photographers.models import Photographer


@pytest.mark.django_db
def test_list_photographers():
    """Проверяем, что API отдает список фотографов."""
    Photographer.objects.create(name="Анна", rating=4.8, hourly_rate=3500, min_hours=2)
    client = APIClient()
    response = client.get("/api/photographers/")
    
    assert response.status_code == 200
    # В DRF пагинация включена, поэтому данные лежат в ключе "results"
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["name"] == "Анна"


@pytest.mark.django_db
def test_create_photographer_unauthorized():
    """Проверяем безопасность: анонимный пользователь не может добавить фотографа."""
    client = APIClient()
    response = client.post("/api/photographers/", {
        "name": "Тест", "rating": 5.0, "hourly_rate": 3000, "min_hours": 1,
    })
    # Ожидаем 401 (Не авторизован), так как в настройках стоит IsAuthenticatedOrReadOnly
    assert response.status_code == 401