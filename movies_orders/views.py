from rest_framework.views import APIView, Response, Request
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie
from rest_framework_simplejwt.authentication import JWTAuthentication

from movies_orders.serializers import MovieOrdersSerializer


class MovieOrdersView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


    def post(self, request: Request, movie_id: int) -> Response:
        found_user = get_object_or_404(Movie.objects.all(), pk=movie_id)
        serializer = MovieOrdersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, movie=found_user)
        return Response(serializer.data, 201)
