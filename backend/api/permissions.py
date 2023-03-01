from rest_framework import permissions


class OwnObjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
