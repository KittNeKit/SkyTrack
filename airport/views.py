from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from airport.models import Airport, Route
from airport.permissions import IsAdminOrIfUserReadOnly
from airport.serializers import AirportSerializer, RouteSerializer


@extend_schema_view(
    list=extend_schema(description="All airport endpoint in the db"),
    retrieve=extend_schema(description="Specific airport endpoint"),
    create=extend_schema(description="Creating airport endpoint"),
)
class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)


@extend_schema_view(
    list=extend_schema(description="All route endpoint in the db"),
    retrieve=extend_schema(description="Specific route endpoint"),
    create=extend_schema(description="Creating route endpoint"),
)
class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)
