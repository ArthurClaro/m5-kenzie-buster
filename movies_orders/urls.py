from django.urls import path

from movies_orders.views import MovieOrdersView


urlpatterns=[
    path("movies/<int:movie_id>/orders/", MovieOrdersView.as_view()),
]