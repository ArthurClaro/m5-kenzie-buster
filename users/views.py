from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, Request
from movies.permissions import IsAdminOrReadOnly, IsUserAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserSerializer

from rest_framework.pagination import PageNumberPagination


class UserView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        user = User.objects.all()
        return Response(UserSerializer(user, many=True).data, 201)

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)


class UserDetailView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = ( IsAuthenticated ,IsUserAdmin ,  )


    def get(self, request: Request, user_id: int) -> Response:
        try:
            found_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, 404)
        self.check_object_permissions(request, found_user)
        serializer = UserSerializer(found_user)
        return Response(serializer.data, 200)

    def patch(self, request: Request, user_id: int) -> Response:
        found_user = get_object_or_404(User.objects.all(), pk=user_id)
        self.check_object_permissions(request, found_user)
        serializer = UserSerializer(found_user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 200)
