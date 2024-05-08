from rest_framework.permissions import BasePermission


class IsAdminAndIsActive(BasePermission):
    """
    Права доступа к API только активных сотрудников(админов).
    """
    message = 'У вас нет прав активного админа!'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and request.user.is_stuff

    def has_object_permission(self, request, view, obj):
        return request.user.is_stuff


class IsOwner(BasePermission):
    """
    Права доступа автора
    """
    message = 'У вас нет прав автора!'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False


class IsSuperUser(BasePermission):
    """
    Права доступа к API главному админу.
    """
    message = 'У вас нет прав суперпользователя!'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsOwnerProfile(BasePermission):
    """
    Права доступа автора профиля
    """
    message = 'Вы не являетесь автором данного профиля!'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False
