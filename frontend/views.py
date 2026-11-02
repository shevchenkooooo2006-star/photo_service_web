"""View-функции для отдачи HTML-страниц с данными из SQLite."""
import sqlite3
from pathlib import Path

from django.shortcuts import render

DB_PATH = Path("data/photo_service.sqlite")


def _query(sql: str, params: tuple = ()) -> list[sqlite3.Row]:
    """Выполнить SQL-запрос и вернуть список строк."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def index(request):
    """Главная страница."""
    return render(request, "index.html")


def photographers_page(request):
    """Страница со списком фотографов (данные из SQLite)."""
    photographers = _query(
        "SELECT id, name, rating, hourly_rate, min_hours "
        "FROM photographers ORDER BY rating DESC;"
    )
    return render(
        request,
        "photographers/photographer_list.html",
        {"photographers": photographers},
    )


def locations_page(request):
    """Страница со списком локаций (данные из SQLite)."""
    locations = _query(
        "SELECT id, name, rent_price FROM locations ORDER BY name;"
    )
    return render(
        request,
        "locations/location_list.html",
        {"locations": locations},
    )


def bookings_page(request):
    """Страница со списком активных бронирований (данные из SQLite, JOIN)."""
    bookings = _query("""
        SELECT
            bookings.id,
            bookings.shoot_date,
            bookings.hours,
            bookings.need_makeup,
            bookings.is_cancelled,
            photographers.name AS photographer_name,
            locations.name AS location_name,
            clients.name AS client_name
        FROM bookings
        JOIN photographers ON bookings.photographer_id = photographers.id
        JOIN locations ON bookings.location_id = locations.id
        JOIN clients ON bookings.client_id = clients.id
        ORDER BY bookings.shoot_date;
    """)
    return render(
        request,
        "bookings/booking_list.html",
        {"bookings": bookings},
    )


def login_page(request):
    """Страница входа."""
    return render(request, "login.html")


def available_photographers(request):
    """Поиск фотографов, свободных на выбранную дату."""
    shoot_date = request.GET.get("date")
    photographers = []
    if shoot_date:
        photographers = _query(
            """
            SELECT id, name, rating, hourly_rate
            FROM photographers
            WHERE id NOT IN (
                SELECT photographer_id
                FROM bookings
                WHERE shoot_date = ? AND is_cancelled = 0
            )
            ORDER BY rating DESC;
            """,
            (shoot_date,),
        )
    return render(
        request,
        "photographers/available.html",
        {"photographers": photographers, "shoot_date": shoot_date},
    )
