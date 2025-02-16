from rest_framework.permissions import BasePermission


class IsAuthenticatedOrCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user
    
class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
    def has_object_permission(self, request, view, obj):
        return obj.branch.restaurant.owner == request.user