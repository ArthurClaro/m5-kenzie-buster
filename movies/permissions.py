from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView

from movies.models import Movie
from users.models import User


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return False


class IsUserAdmin(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: User):

        return request.user.is_authenticated and (obj == request.user or request.user.is_superuser)
