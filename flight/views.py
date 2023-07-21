from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from airport.permissions import IsAdminOrIfUserReadOnly
from flight.models import AirplaneType, Airplane, Crew, Flight
from flight.serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer,
    FlightSerializer,
)


@extend_schema_view(
    list=extend_schema(description="All airplane type endpoint in the db"),
    create=extend_schema(description="Creating airplane type endpoint"),
)
class AirplaneTypeViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)


@extend_schema_view(
    list=extend_schema(description="All airplane endpoint in the db"),
    retrieve=extend_schema(description="Specific airplane endpoint"),
    create=extend_schema(description="Creating airplane endpoint"),
)
class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)


@extend_schema_view(
    list=extend_schema(description="All crew endpoint in the db"),
    create=extend_schema(description="Creating crew endpoint"),
)
class CrewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)


@extend_schema_view(
    list=extend_schema(description="All flight endpoint in the db"),
    retrieve=extend_schema(description="Specific flight endpoint"),
    create=extend_schema(description="Creating flight endpoint"),
)
class FlightViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Flight.objects.prefetch_related("crew").select_related("route")
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)
