from django.db import models


class RatingMovies(models.TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, default="", blank=True)
    rating = models.CharField(
        max_length=20, choices=RatingMovies.choices, default=RatingMovies.G
    )
    synopsis = models.TextField(default="", blank=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies"
    )

    movies_orders = models.ManyToManyField(
        "users.User", through="movies_orders.MovieOrder", related_name="movies_orders"
    )
