from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS
User = get_user_model()

class AllowAllPermission(BasePermission):
    def has_permission(self, request, view):
        return True


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role != User.Role.CLIENT:
            return False
        return request.user.is_active

class SupplierPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role != User.Role.SUPPLIER:
            return False
        return request.user.is_active

class AuthorPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role != User.Role.AUTHOR:
            return False
        return request.user.is_active

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role != User.Role.ADMIN:
            return False
        return request.user.is_active