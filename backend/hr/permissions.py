from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'employee'

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role in ['customer']
