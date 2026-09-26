from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.access_control.models import User

from .factories import DEFAULT_PASSWORD, create_manager, create_receptionist


class ReceptionistManagementApiTests(APITestCase):
    def setUp(self):
        self.manager = create_manager()
        self.receptionist = create_receptionist()
        self.list_url = reverse("access_control:receptionists")

    def test_manager_can_list_receptionists(self):
        self.client.force_authenticate(self.manager)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], self.receptionist.username)

    def test_manager_can_create_receptionist(self):
        self.client.force_authenticate(self.manager)

        response = self.client.post(
            self.list_url,
            {
                "username": "recepcao.dois",
                "name": "Recepcionista Dois",
                "password": "Outra@123",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = User.objects.get(username="recepcao.dois")
        self.assertEqual(created.role, User.Role.RECEPTIONIST)
        self.assertTrue(created.check_password("Outra@123"))

    def test_receptionist_cannot_list_or_create_accounts(self):
        self.client.force_authenticate(self.receptionist)

        list_response = self.client.get(self.list_url)
        create_response = self.client.post(
            self.list_url,
            {
                "username": "indevido",
                "name": "Acesso Indevido",
                "password": "Outra@123",
            },
            format="json",
        )

        self.assertEqual(list_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(User.objects.filter(username="indevido").exists())

    def test_manager_can_deactivate_receptionist_and_end_session(self):
        self.receptionist.active_session_key = "session-key"
        self.receptionist.save(update_fields=["active_session_key"])
        self.client.force_authenticate(self.manager)
        detail_url = reverse(
            "access_control:receptionist-detail", kwargs={"pk": self.receptionist.pk}
        )

        response = self.client.patch(detail_url, {"is_active": False}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.receptionist.refresh_from_db()
        self.assertFalse(self.receptionist.is_active)
        self.assertEqual(self.receptionist.active_session_key, "")

    def test_manager_can_reset_receptionist_password(self):
        self.client.force_authenticate(self.manager)
        reset_url = reverse(
            "access_control:receptionist-reset-password",
            kwargs={"pk": self.receptionist.pk},
        )

        response = self.client.post(reset_url, {"password": "NovaSenha@2"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.receptionist.refresh_from_db()
        self.assertTrue(self.receptionist.check_password("NovaSenha@2"))

    def test_weak_password_is_rejected(self):
        self.client.force_authenticate(self.manager)

        response = self.client.post(
            self.list_url,
            {
                "username": "recepcao.fraca",
                "name": "Senha Fraca",
                "password": "12345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_anonymous_user_cannot_access_receptionists(self):
        response = self.client.get(self.list_url)

        self.assertIn(
            response.status_code,
            {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN},
        )

    def test_receptionist_creation_does_not_accept_manager_role(self):
        self.client.force_authenticate(self.manager)

        response = self.client.post(
            self.list_url,
            {
                "username": "novo.gestor",
                "name": "Novo Gestor",
                "password": DEFAULT_PASSWORD,
                "role": User.Role.MANAGER,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="novo.gestor").role, User.Role.RECEPTIONIST)
