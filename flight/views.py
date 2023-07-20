from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from airport.permissions import IsAdminOrIfUserReadOnly
from flight.models import AirplaneType, Airplane, Crew, Flight
from flight.serializers import AirplaneTypeSerializer, AirplaneSerializer, CrewSerializer, FlightSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all().select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().prefetch_related("crew").select_related("route")
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)
