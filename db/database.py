"""Модуль подключения к базе данных SQLite."""
import sqlite3

DB_PATH = "data/photo_service.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать подключение к базе данных с включённой проверкой внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
