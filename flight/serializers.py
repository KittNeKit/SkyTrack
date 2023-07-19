from rest_framework import serializers

from airport.models import Route
from flight.models import AirplaneType, Airplane, Crew, Flight


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        queryset=AirplaneType.objects.all()
        )

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class FlightSerializer(serializers.ModelSerializer):
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="full_name",
        queryset=Crew.objects.all()
        )
    route = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="route_str",
        queryset=Route.objects.all()
        )
    airplane = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="airplane_name",
        queryset=Airplane.objects.all()
        )

    class Meta:
        model = Flight
        fields = (
            "crew",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )
