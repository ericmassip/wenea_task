from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from chargepoints.models import Chargepoint


class ChargepointListTests(APITestCase):
    def test_list(self):
        Chargepoint.objects.bulk_create([Chargepoint(name="CP1"), Chargepoint(name="CP2")])

        response = self.client.get(reverse("01:chargepoint-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["name"] == "CP1"
        assert response.data[1]["name"] == "CP2"

    def test_create(self):
        user = User.objects.create_user(username="test", password="test")
        self.client.force_login(user=user)

        Chargepoint.objects.bulk_create([Chargepoint(name="CP1"), Chargepoint(name="CP2")])

        response = self.client.post(reverse("01:chargepoint-list"), data={"name": "CP3"})
        assert response.status_code == status.HTTP_201_CREATED
        assert Chargepoint.objects.count() == 3
        assert Chargepoint.objects.get(name="CP3")


class ChargepointDetailTests(APITestCase):
    def test_detail(self):
        Chargepoint.objects.create(id=1, name="CP1", status=Chargepoint.Status.CHARGING)

        response = self.client.get(reverse("01:chargepoint-detail", kwargs={"pk": 1}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "CP1"
        assert response.data["status"] == Chargepoint.Status.CHARGING

    def test_delete_happy_path(self):
        user = User.objects.create_user(username="test", password="test")
        self.client.force_login(user=user)

        chargepoint = Chargepoint.objects.create(id=1, name="CP1")

        response = self.client.delete(reverse("01:chargepoint-detail", kwargs={"pk": 1}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        chargepoint.refresh_from_db()
        assert chargepoint.is_deleted()

    def test_cannot_redelete_deleted_chargepoint(self):
        user = User.objects.create_user(username="test", password="test")
        self.client.force_login(user=user)

        chargepoint = Chargepoint.objects.create(id=1, name="CP1")
        chargepoint.deleted_at = timezone.now()
        chargepoint.save()

        response = self.client.delete(reverse("01:chargepoint-detail", kwargs={"pk": 1}))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data[0]) == "CP1 cannot be updated/deleted because it is already deleted"

    def test_update_happy_path(self):
        user = User.objects.create_user(username="test", password="test")
        self.client.force_login(user=user)

        chargepoint = Chargepoint.objects.create(id=1, name="CP1", status=Chargepoint.Status.CHARGING)

        response = self.client.put(reverse("01:chargepoint-detail", kwargs={"pk": 1}), data={"name": "CP1", "status": Chargepoint.Status.READY})
        assert response.status_code == status.HTTP_200_OK
        chargepoint.refresh_from_db()
        assert chargepoint.status == Chargepoint.Status.READY

    def test_cannot_update_deleted_chargepoint(self):
        user = User.objects.create_user(username="test", password="test")
        self.client.force_login(user=user)

        chargepoint = Chargepoint.objects.create(id=1, name="CP1", status=Chargepoint.Status.CHARGING)
        chargepoint.deleted_at = timezone.now()
        chargepoint.save()

        response = self.client.put(reverse("01:chargepoint-detail", kwargs={"pk": 1}), data={"name": "CP1", "status": Chargepoint.Status.READY})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data[0]) == "CP1 cannot be updated/deleted because it is already deleted"
