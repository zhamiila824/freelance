from rest_framework import permissions


class WriteTask(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.role == 'customer':
            return True
        return False


class DoTask(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.role == 'executor':
            return True
        return False
