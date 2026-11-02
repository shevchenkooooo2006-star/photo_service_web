from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from frontend import views as frontend_views

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # --- API ---
    path("api/", include("api.urls")),
    
    # --- Документация API (Swagger) ---
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    
    # --- Frontend ---
    path("", frontend_views.index, name="index"),
    path("photographers/", frontend_views.photographers_page, name="photographers"),
    path("locations/", frontend_views.locations_page, name="locations"),
    path("bookings/", frontend_views.bookings_page, name="bookings"),
    path("login/", frontend_views.login_page, name="login"),
]