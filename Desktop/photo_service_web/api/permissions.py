"""Кастомные права доступа."""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Изменять может только владелец или админ."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or getattr(obj, "user", None) == request.user


class IsBookingOwner(permissions.BasePermission):
    """Бронирование может изменять только его создатель."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # админ может всё
        if request.user.is_staff:
            return True
        # клиент владелец
        if obj.client.user == request.user:
            return True
        return False