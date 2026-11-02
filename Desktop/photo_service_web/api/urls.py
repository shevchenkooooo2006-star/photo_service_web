"""Маршруты REST API."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from .views import (
    PhotographerViewSet, LocationViewSet,
    ClientViewSet, BookingViewSet, RegisterView,
)

router = DefaultRouter()
router.register(r"photographers", PhotographerViewSet, basename="photographer")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"clients", ClientViewSet, basename="client")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]