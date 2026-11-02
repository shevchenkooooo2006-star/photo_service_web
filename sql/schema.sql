-- =============================================
-- Сервис организации фотосессий: структура БД
-- =============================================

CREATE TABLE IF NOT EXISTS photographers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rating REAL NOT NULL,
    hourly_rate REAL NOT NULL,
    min_hours INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rent_price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    photographer_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    shoot_date TEXT NOT NULL,
    hours INTEGER NOT NULL,
    need_makeup INTEGER NOT NULL DEFAULT 0,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (photographer_id) REFERENCES photographers(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);