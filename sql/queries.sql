-- =============================================
-- ЗАПРОСЫ ПРОЕКТА «СЕРВИС ОРГАНИЗАЦИИ ФОТОСЕССИЙ»
-- =============================================

-- ЗАПРОС 1. Список всех фотографов (сортировка по рейтингу)
SELECT id, name, rating, hourly_rate, min_hours
FROM photographers
ORDER BY rating DESC;

-- ЗАПРОС 2. Список всех локаций (сортировка по цене)
SELECT id, name, rent_price
FROM locations
ORDER BY rent_price ASC;

-- ЗАПРОС 3. Поиск фотографов с рейтингом не ниже заданного (WHERE)
SELECT id, name, rating
FROM photographers
WHERE rating >= 4.5
ORDER BY rating DESC;

-- ЗАПРОС 4. Поиск локаций с арендой не выше заданной (WHERE)
SELECT id, name, rent_price
FROM locations
WHERE rent_price <= 1500
ORDER BY rent_price ASC;

-- ЗАПРОС 5. Активные бронирования с JOIN: клиент, фотограф, локация (JOIN)
SELECT
    bookings.id,
    bookings.shoot_date,
    photographers.name AS photographer_name,
    locations.name AS location_name,
    clients.name AS client_name
FROM bookings
JOIN photographers ON bookings.photographer_id = photographers.id
JOIN locations ON bookings.location_id = locations.id
JOIN clients ON bookings.client_id = clients.id
WHERE bookings.is_cancelled = 0
ORDER BY bookings.shoot_date;

-- ЗАПРОС 6. Все бронирования конкретного клиента (JOIN + WHERE)
SELECT
    bookings.id,
    bookings.shoot_date,
    photographers.name AS photographer_name,
    locations.name AS location_name
FROM bookings
JOIN photographers ON bookings.photographer_id = photographers.id
JOIN locations ON bookings.location_id = locations.id
WHERE bookings.client_id = 1
ORDER BY bookings.shoot_date DESC;

-- ЗАПРОС 7. Общее количество фотографов (агрегат COUNT)
SELECT COUNT(*) AS total_photographers
FROM photographers;

-- ЗАПРОС 8. Количество активных бронирований (агрегат COUNT + WHERE)
SELECT COUNT(*) AS active_bookings
FROM bookings
WHERE is_cancelled = 0;

-- ЗАПРОС 9. Количество бронирований по каждому фотографу (GROUP BY)
SELECT
    photographers.name AS photographer_name,
    COUNT(bookings.id) AS bookings_count
FROM photographers
LEFT JOIN bookings ON photographers.id = bookings.photographer_id
    AND bookings.is_cancelled = 0
GROUP BY photographers.id, photographers.name
ORDER BY bookings_count DESC;

-- ЗАПРОС 10. Топ фотографов по количеству броней (GROUP BY + HAVING)
SELECT
    photographers.name AS photographer_name,
    COUNT(bookings.id) AS bookings_count
FROM photographers
JOIN bookings ON photographers.id = bookings.photographer_id
WHERE bookings.is_cancelled = 0
GROUP BY photographers.id, photographers.name
HAVING COUNT(bookings.id) >= 1
ORDER BY bookings_count DESC;