from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from flight.models import Flight
from flight.serializers import FlightSerializer
from flight.tests.test_airplane_api import sample_airplane
from flight.tests.test_crew_api import sample_crew
from airport.tests.test_route_api import sample_route

FLIGHT_URL = reverse("departures:flight-list")


def sample_flight(**params):
    defaults = {
        "route": sample_route(),
        "airplane": sample_airplane(),
        "departure_time": "2006-12-05T21:00:00Z",
        "arrival_time": "2023-07-20T16:00:00Z",
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)


def detail_url(flight_id):
    return reverse("departures:flight-detail", args=[flight_id])


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_flight(self):
        sample_flight()
        sample_flight()

        res = self.client.get(FLIGHT_URL)

        flight = Flight.objects.order_by("id")
        serializer = FlightSerializer(flight, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_flight_detail(self):
        flight = sample_flight()

        url = detail_url(flight.id)
        res = self.client.get(url)

        serializer = FlightSerializer(flight)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_flight_forbidden(self):
        payload = {
            "crew": sample_crew(),
            "route": sample_route(),
            "airplane": sample_airplane(),
            "departure_time": "2006-12-05 21:00:00",
            "arrival_time": "2023-07-20 16:00:00",
        }
        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_flight(self):
        payload = {
            "crew": [sample_crew().id],
            "route": sample_route().id,
            "airplane": sample_airplane().id,
            "departure_time": "2006-12-05 21:00:00",
            "arrival_time": "2023-07-20 16:00:00",
        }

        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_put_flight_not_allowed(self):
        payload = {
            "crew": sample_crew(),
            "route": sample_route(),
            "airplane": sample_airplane(),
            "departure_time": "2006-12-05 21:00:00",
            "arrival_time": "2023-07-20 16:00:00",
        }

        flight = sample_flight()
        url = detail_url(flight.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_flight_not_allowed(self):
        flight = sample_flight()
        url = detail_url(flight.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
