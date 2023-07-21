from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from airport.models import Route
from airport.serializers import RouteSerializer
from airport.tests.test_airport_api import sample_airport

ROUTE_URL = reverse("route:route-list")


def sample_route(**params):
    defaults = {
        "source": sample_airport(),
        "destination": sample_airport(),
        "distance": 300,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def detail_url(route_id):
    return reverse("route:route-detail", args=[route_id])


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_route(self):
        sample_route()
        sample_route()

        res = self.client.get(ROUTE_URL)

        route = Route.objects.order_by("id")
        serializer = RouteSerializer(route, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_route_detail(self):
        route = sample_route()

        url = detail_url(route.id)
        res = self.client.get(url)

        serializer = RouteSerializer(route)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_route_forbidden(self):
        payload = {
            "source": sample_airport(),
            "destination": sample_airport(),
            "distance": 403,
        }
        res = self.client.post(ROUTE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_put_route_not_allowed(self):
        payload = {
            "source": sample_airport().id,
            "destination": sample_airport().id,
            "distance": 405,
        }

        route = sample_route()
        url = detail_url(route.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_route_not_allowed(self):
        route = sample_route()
        url = detail_url(route.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
