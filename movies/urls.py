from django.urls import path
from movies.views import MovieDetailView, MovieView


urlpatterns=[
    path("movies/", MovieView.as_view()),
    path("movies/<int:movies_id>/", MovieDetailView.as_view()),
]
    
