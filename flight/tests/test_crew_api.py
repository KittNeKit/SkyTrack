from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from flight.models import Crew
from flight.serializers import CrewSerializer

CREW_URL = reverse("flight:crew-list")


def sample_crew(**params):
    defaults = {
        "first_name": "Test name",
        "last_name": "Test last name"
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_crew(self):
        sample_crew()
        sample_crew()

        res = self.client.get(CREW_URL)

        crew = Crew.objects.order_by("id")
        serializer = CrewSerializer(crew, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_crew_forbidden(self):
        payload = {
            "first_name": "Test Forbidden",
            "last_name": "Forbidden"
        }
        res = self.client.post(CREW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_crew(self):
        payload = {
            "first_name": "Test",
            "last_name": "201"
        }
        res = self.client.post(CREW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        crew = Crew.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(crew, key))
