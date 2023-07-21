from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from airport.models import Airport
from airport.serializers import AirportSerializer

AIRPORT_URL = reverse("route:airport-list")


def sample_airport(**params):
    defaults = {
        "name": "Test airport",
        "closest_bit_city": "Test City",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def detail_url(airport_id):
    return reverse("route:airport-detail", args=[airport_id])


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airport(self):
        sample_airport()
        sample_airport()

        res = self.client.get(AIRPORT_URL)

        airport = Airport.objects.order_by("id")
        serializer = AirportSerializer(airport, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_airport_detail(self):
        airport = sample_airport()

        url = detail_url(airport.id)
        res = self.client.get(url)

        serializer = AirportSerializer(airport)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airport_forbidden(self):
        payload = {
            "name": "Test Forbidden",
            "closest_bit_city": "Test Forbidden",
        }
        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airport(self):
        payload = {
            "name": "Test airport",
            "closest_bit_city": "Test City",
        }
        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airport = Airport.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(airport, key))

    def test_put_airport_not_allowed(self):
        payload = {
            "name": "Test airport",
            "closest_bit_city": "Test City",
        }

        airport = sample_airport()
        url = detail_url(airport.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_airport_not_allowed(self):
        airport = sample_airport()
        url = detail_url(airport.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
