"""Перенос данных из JSON-файлов в SQLite."""
import json
from pathlib import Path

from db.database import get_connection

DATA_DIR = Path("data")


def load_json(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def import_photographers(conn) -> None:
    """Перенести фотографов."""
    photographers = load_json("photographers.json")
    if not photographers:
        return
    conn.executemany(
        """
        INSERT OR REPLACE INTO photographers
        (id, name, rating, hourly_rate, min_hours)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (p["id"], p["name"], p["rating"], p["hourly_rate"], p["min_hours"])
            for p in photographers
        ],
    )


def import_locations(conn) -> None:
    """Перенести локации."""
    locations = load_json("locations.json")
    if not locations:
        return
    conn.executemany(
        """
        INSERT OR REPLACE INTO locations
        (id, name, rent_price)
        VALUES (?, ?, ?)
        """,
        [(loc["id"], loc["name"], loc["rent_price"]) for loc in locations],
    )


def import_clients(conn) -> None:
    """Перенести клиентов."""
    clients = load_json("clients.json")
    if not clients:
        return
    conn.executemany(
        """
        INSERT OR REPLACE INTO clients
        (id, name, email)
        VALUES (?, ?, ?)
        """,
        [(c["id"], c["name"], c["email"]) for c in clients],
    )


def import_bookings(conn) -> None:
    """Перенести бронирования."""
    bookings = load_json("bookings.json")
    if not bookings:
        return
    conn.executemany(
        """
        INSERT OR REPLACE INTO bookings
        (id, photographer_id, location_id, client_id,
         shoot_date, hours, need_makeup, is_cancelled)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                b["id"],
                b["photographer_id"],
                b["location_id"],
                b["client_id"],
                b["shoot_date"],
                b["hours"],
                int(b.get("need_makeup", False)),
                int(b.get("is_cancelled", False)),
            )
            for b in bookings
        ],
    )


def main() -> None:
    conn = get_connection()
    try:
        import_photographers(conn)
        import_locations(conn)
        import_clients(conn)
        import_bookings(conn)
        conn.commit()
        print("Импорт завершён.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
