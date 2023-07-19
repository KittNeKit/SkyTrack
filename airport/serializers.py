from rest_framework import serializers

from airport.models import Airport, Route


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_bit_city")


class RouteSerializer(serializers.ModelSerializer):
    source = AirportSerializer(many=False, read_only=False)
    destination = AirportSerializer(many=False, read_only=False)

    class Meta:
        model = Route
        fields = ("source", "destination", "distance")
