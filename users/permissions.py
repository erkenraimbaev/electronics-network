from rest_framework.permissions import BasePermission
from users.models import UserRole


class IsActive(BasePermission):
    """
    Права доступа к API только активных сотрудников.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active


class IsAdmin(BasePermission):
    """
    Права доступа админа
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.role == UserRole.ADMIN


class IsOwner(BasePermission):
    """
    Права доступа автора
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
