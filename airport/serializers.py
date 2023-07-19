from rest_framework import serializers

from airport.models import Airport, Route


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_bit_city")


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        queryset=Airport.objects.all()
        )
    destination = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        queryset=Airport.objects.all()
        )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")
