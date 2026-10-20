"""View-функции для отдачи HTML-страниц."""
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def photographers_page(request):
    return render(request, "photographers.html")


def locations_page(request):
    return render(request, "locations.html")


def bookings_page(request):
    return render(request, "bookings.html")


def login_page(request):
    return render(request, "login.html")