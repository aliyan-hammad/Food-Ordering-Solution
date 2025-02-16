from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAllowAny(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return request.user.is_authenticated

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_superuser