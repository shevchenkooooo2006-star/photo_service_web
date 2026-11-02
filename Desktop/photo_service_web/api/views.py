from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from users.models import Client
from photographers.models import Photographer
from locations.models import Location
from bookings.models import Booking

from .serializers import (
    PhotographerSerializer, LocationSerializer, 
    ClientSerializer, BookingSerializer, RegisterSerializer
)


class RegisterView(APIView):
    """Регистрация нового пользователя."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotographerViewSet(viewsets.ModelViewSet):
    """CRUD для фотографов."""
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """CRUD для локаций."""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """CRUD для клиентов."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """CRUD для бронирований."""
    queryset = Booking.objects.select_related("photographer", "location", "client").all()
    serializer_class = BookingSerializer

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.cancel()
        return Response({"status": "cancelled"})