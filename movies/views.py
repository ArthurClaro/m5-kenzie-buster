from rest_framework.views import APIView, Response, Request

from movies.models import Movie
from movies.permissions import IsAdminOrReadOnly
from movies.serializers import MovieSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView,PageNumberPagination):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request: Request) -> Response:
        movie = Movie.objects.all()
        
        result_page = self.paginate_queryset(movie, request, view=self)
        serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)
    

   

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, 201)


class MovieDetailView(APIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = ( IsAdminOrReadOnly,)

    def get(self, request: Request, movies_id: int) -> Response:
        try:
            found_movie = Movie.objects.get(pk=movies_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        serializer = MovieSerializer(found_movie)
        return Response(serializer.data, 200)
    
    def delete(self, request: Request, movies_id: int) -> Response:
        try:
            found_movie = Movie.objects.get(pk=movies_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        found_movie.delete()
        return Response(status=204)
