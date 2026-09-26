from datetime import timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.access_control.models import LoginAttempt

from .factories import DEFAULT_PASSWORD, create_manager


class AuthenticationApiTests(APITestCase):
    def setUp(self):
        self.manager = create_manager()
        self.csrf_url = reverse("access_control:csrf")
        self.login_url = reverse("access_control:login")
        self.me_url = reverse("access_control:current-user")
        self.logout_url = reverse("access_control:logout")

    def login(self, client=None, password=DEFAULT_PASSWORD):
        active_client = client or self.client
        csrf_response = active_client.get(self.csrf_url)
        token = csrf_response.data["csrfToken"]
        return active_client.post(
            self.login_url,
            {"username": self.manager.username, "password": password},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

    def test_login_requires_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)

        response = client.post(
            self.login_url,
            {"username": self.manager.username, "password": DEFAULT_PASSWORD},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_credentials_create_session(self):
        response = self.login()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], "MANAGER")
        self.assertIn("sessionid", self.client.cookies)
        self.manager.refresh_from_db()
        self.assertTrue(self.manager.active_session_key)

    def test_invalid_credentials_are_rejected_without_exposing_username(self):
        response = self.login(password="SenhaErrada@1")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Nome de usuário ou senha inválidos.")

    def test_five_failures_temporarily_block_login(self):
        for _ in range(settings.LOGIN_FAILURE_LIMIT):
            response = self.login(password="SenhaErrada@1")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        blocked_response = self.login()

        self.assertEqual(blocked_response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        attempt = LoginAttempt.objects.get(username=self.manager.username)
        self.assertGreater(attempt.locked_until, timezone.now())

    def test_login_is_allowed_after_lockout_expires(self):
        LoginAttempt.objects.create(
            username=self.manager.username,
            failed_attempts=settings.LOGIN_FAILURE_LIMIT,
            locked_until=timezone.now() - timedelta(seconds=1),
        )

        response = self.login()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(LoginAttempt.objects.filter(username=self.manager.username).exists())

    def test_new_login_invalidates_previous_session(self):
        first_client = APIClient()
        second_client = APIClient()
        self.assertEqual(self.login(first_client).status_code, status.HTTP_200_OK)
        self.assertEqual(self.login(second_client).status_code, status.HTTP_200_OK)

        old_session_response = first_client.get(self.me_url)
        current_session_response = second_client.get(self.me_url)

        self.assertIn(
            old_session_response.status_code,
            {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN},
        )
        self.assertEqual(current_session_response.status_code, status.HTTP_200_OK)

    def test_logout_invalidates_current_session(self):
        self.login()
        csrf_token = self.client.cookies["csrftoken"].value

        response = self.client.post(self.logout_url, HTTP_X_CSRFTOKEN=csrf_token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn(
            self.client.get(self.me_url).status_code,
            {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN},
        )
        self.manager.refresh_from_db()
        self.assertEqual(self.manager.active_session_key, "")

    def test_session_inactivity_limit_is_fifteen_minutes(self):
        self.assertEqual(settings.SESSION_COOKIE_AGE, 15 * 60)
        self.assertTrue(settings.SESSION_SAVE_EVERY_REQUEST)
