# Сервис организации фотосессий (Web)

Веб-приложение для управления фотографами, локациями и бронированием фотосессий. 
Проект разработан в рамках дисциплины «Технологии разработки приложений на базе фреймворков».

## Возможности

- Просмотр, поиск и фильтрация фотографов;
- Просмотр локаций;
- Создание и отмена бронирований;
- Разграничение прав доступа (JWT-аутентификация);
- REST API с автоматической документацией Swagger;
- Административная панель Django для управления данными.

## Технологии

- **Backend:** Python 3.10, Django 4.2, Django REST Framework (DRF);
- **База данных:** SQLite (для разработки);
- **Аутентификация:** JWT (SimpleJWT);
- **Frontend:** HTML5, Bootstrap 5, JavaScript (Fetch API);
- **Тестирование:** Pytest, Pytest-django;
- **Документация API:** drf-spectacular (Swagger UI).

## Структура проекта

- `config/` — настройки проекта и главный файл маршрутизации;
- `users/`, `photographers/`, `locations/`, `bookings/` — Django-приложения с моделями предметной области;
- `api/` — REST API (сериализаторы, ViewSets);
- `frontend/` — HTML-шаблоны и статика (JS);
- `tests/` — автоматизированные тесты;
- `data/` — JSON-файлы (для миграции старых данных).

## Установка и запуск

1. Клонируйте репозиторий:
   bash
   git clone <ссылка>
   cd photo_service_web

## Django ORM (ПР9)

Данные проекта теперь получаются через Django ORM, а не через ручные SQL-запросы.

### Реализовано
- Модели `Photographer`, `Location`, `Client`, `Booking` с миграциями.
- Замена SQL-запросов на ORM-методы: `all()`, `filter()`, `exclude()`, `get()`, `order_by()`, `values()`, `select_related()`, `aggregate()`, `annotate()`.
- Пагинация списка броней (`Paginator`, 5 записей на страницу).
- Проверка доступности фотографов через `exclude()` и `values_list()`.

### Файлы
- `frontend/views.py` — представления переведены на ORM.
- `bookings/templates/bookings/booking_list.html` — добавлена пагинация.
- ORM-запросы продемонстрированы в `python manage.py shell`.

## Админка и Django Debug Toolbar (ПР10)

- Настроены списки, поиск, фильтры для моделей Photographer, Location, Booking, Client.
- Добавлена локализация админки (`ru-RU`).
- Подключён Django Debug Toolbar для анализа SQL-запросов.
- В админке используются `list_editable`, `search_fields`, `list_filter`, `autocomplete_fields`, `date_hierarchy`.

## RESTful API (ПР11)

### Ресурсы и методы
- `/api/photographers/` — CRUD фотографов (GET, POST, PUT, PATCH, DELETE).
- `/api/locations/` — CRUD локаций.
- `/api/clients/` — CRUD клиентов.
- `/api/bookings/` — CRUD броней.
- `/api/bookings/{id}/cancel/` — POST-запрос для отмены брони.

### Аутентификация
- JWT-токены: `/api/auth/token/`, `/api/auth/token/refresh/`.
- Регистрация: `/api/auth/register/`.

### Документация
- Swagger UI: `/api/docs/`.
- OpenAPI схема: `/api/schema/`.

### Безопасность
- JWT + IsAuthenticatedOrReadOnly.
- CORS (доверенные origins).
- Throttling (30/мин для анонимов, 120/мин для авторизованных).
- Секреты в `.env`.
- ORM (защита от SQL-инъекций).

### Форматы данных
- Все запросы и ответы — JSON.
- В сериализаторах реализованы валидация и вложенные данные (`photographer_detail` и т.д.).