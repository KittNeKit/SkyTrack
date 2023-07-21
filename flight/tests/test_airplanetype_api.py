from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airport
from flight.models import AirplaneType
from flight.serializers import AirplaneTypeSerializer

AIRPLANE_TYPE_URL = reverse("departures:airplanetype-list")


def sample_airplane_type(**params):
    defaults = {
        "name": "Test airplane",
    }
    defaults.update(params)

    return AirplaneType.objects.create(**defaults)


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        res = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplane_type(self):
        sample_airplane_type()
        sample_airplane_type()

        res = self.client.get(AIRPLANE_TYPE_URL)

        airplane_type = AirplaneType.objects.order_by("id")
        serializer = AirplaneTypeSerializer(airplane_type, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airplane_type_forbidden(self):
        payload = {
            "name": "Test Forbidden",
        }
        res = self.client.post(AIRPLANE_TYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane_type(self):
        payload = {
            "name": "Test airplane type",
        }
        res = self.client.post(AIRPLANE_TYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airplane_type = AirplaneType.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(airplane_type, key))
