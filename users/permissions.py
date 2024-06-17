from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderators").exists:
            return True
        return "У вас нет прав, доступно только модераторам!"


class IsNotModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user or request.user.is_superuser:
            return True
        return "У вас нет прав, доступно только владельцу!"


class IsAuth(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id:
            return True
        return "Вы не обладаете достаточными правами для данного действия"
