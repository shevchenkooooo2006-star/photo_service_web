from django.shortcuts import render
from django.core.paginator import Paginator
from photographers.models import Photographer
from locations.models import Location
from bookings.models import Booking
from datetime import datetime


def index(request):
    return render(request, "index.html")


def photographers_page(request):
    """Страница со списком фотографов."""
    photographers = Photographer.objects.all().order_by("-rating")
    context = {
        "photographers": photographers,
    }
    return render(request, "photographers/photographer_list.html", context)


def locations_page(request):
    locations = Location.objects.all().order_by("name")
    return render(request, "locations/location_list.html", {"locations": locations})


def bookings_page(request):
    bookings = Booking.objects.select_related(
        "photographer", "location", "client"
    ).order_by("-shoot_date")

    # Пагинация: 5 записей на страницу
    paginator = Paginator(bookings, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "bookings/booking_list.html", {"page_obj": page_obj})


def available_photographers(request):
    shoot_date_raw = request.GET.get("date", "").strip()
    shoot_date = None
    error = None
    photographers = Photographer.objects.all().order_by("-rating")

    if shoot_date_raw:
        try:
            # Проверяем, что введённая строка — дата в формате YYYY-MM-DD
            shoot_date = datetime.strptime(shoot_date_raw, "%Y-%m-%d").date()

            # Ищем занятых фотографов на эту дату
            busy_ids = Booking.objects.filter(
                shoot_date=shoot_date,
                is_cancelled=False,
            ).values_list("photographer_id", flat=True)

            photographers = photographers.exclude(id__in=busy_ids)

        except ValueError:
            # Если дата некорректна — не падаем, а показываем ошибку
            error = f"Некорректная дата: «{shoot_date_raw}». Используйте формат ГГГГ-ММ-ДД."

    return render(
        request,
        "photographers/available.html",
        {
            "photographers": photographers,
            "shoot_date": shoot_date_raw,
            "error": error,
        },
    )


def login_page(request):
    return render(request, "login.html")
