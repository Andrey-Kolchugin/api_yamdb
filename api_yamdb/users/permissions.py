from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    """
    Проверяет является ли пользователь админом,
    модератором или просит информацию о себе.
    """

    def has_permission(self, request, view):
        if view.action in ('retrieve', 'partial_update'):
            return True
        if view.action == 'destroy':
            return True
        return request.user.is_authenticated and (
            request.user.role == 'admin'
            or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve', 'partial_update', ):
            return (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )
