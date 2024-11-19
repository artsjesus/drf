from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
        Проверяет, что пользователь является модератором.
        """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, что пользователь является владельцем.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False