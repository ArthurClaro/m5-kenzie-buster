from rest_framework import serializers

from movies.models import Movie, RatingMovies


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, default="", allow_null=True)
    rating = serializers.ChoiceField(
         choices=RatingMovies.choices, default=RatingMovies.G
    )
    synopsis = serializers.CharField(default="", allow_null=True)

    added_by = serializers.EmailField(read_only=True, source="user.email")

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
