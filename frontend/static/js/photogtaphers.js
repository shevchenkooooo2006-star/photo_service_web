{% extends "base.html" %}
{% load static %}

{% block content %}
<h2>Фотографы</h2>
<div class="row mb-3">
    <div class="col-md-4">
        <input type="text" id="search" class="form-control" placeholder="Поиск по имени">
    </div>
</div>
<div id="photographers-list" class="row"></div>
{% endblock %}

{% block scripts %}
<script>
    // Ждем полной загрузки страницы
    window.addEventListener('load', function() {
        console.log("Страница загружена, ищем контейнер...");
        const container = document.getElementById("photographers-list");
        
        if (!container) {
            console.error("Контейнер не найден!");
            return;
        }

        fetch("/api/photographers/")
            .then(res => {
                if (!res.ok) throw new Error("Ошибка сервера: " + res.status);
                return res.json();
            })
            .then(data => {
                console.log("Данные получены:", data);
                const photographers = data.results || data;
                container.innerHTML = "";

                photographers.forEach(p => {
                    container.innerHTML += `
                        <div class="col-md-4 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <h5>${p.name}</h5>
                                    <p>⭐ Рейтинг: ${p.rating}</p>
                                    <p>💰 ${p.hourly_rate} руб./ч</p>
                                    <p>⏱ Мин. часов: ${p.min_hours}</p>
                                </div>
                            </div>
                        </div>`;
                });
            })
            .catch(err => {
                console.error("Ошибка при загрузке данных:", err);
                container.innerHTML = `<p class="text-danger">Ошибка загрузки: ${err.message}</p>`;
            });
    });
</script>
{% endblock %}