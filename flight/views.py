from rest_framework import viewsets

from flight.models import AirplaneType, Airplane, Crew, Flight
from flight.serializers import AirplaneTypeSerializer, AirplaneSerializer, CrewSerializer, FlightSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all().select_related("airplane_type")
    serializer_class = AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().prefetch_related("crew").select_related("route")
    serializer_class = FlightSerializer
