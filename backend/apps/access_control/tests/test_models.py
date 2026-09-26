from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.access_control.models import User

from .factories import DEFAULT_PASSWORD, create_manager


class UserModelTests(TestCase):
    def test_normalizes_username(self):
        user = User.objects.create_user(
            username="  Recepcao.Um ",
            name="Recepcionista Um",
            password=DEFAULT_PASSWORD,
            role=User.Role.RECEPTIONIST,
        )

        self.assertEqual(user.username, "recepcao.um")

    def test_superuser_is_always_manager(self):
        user = User.objects.create_superuser(
            username="admin",
            name="Gestor",
            password=DEFAULT_PASSWORD,
        )

        self.assertEqual(user.role, User.Role.MANAGER)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_password_policy_accepts_strong_password(self):
        password_validation.validate_password(DEFAULT_PASSWORD, create_manager())

    def test_password_policy_rejects_each_missing_character_group(self):
        invalid_passwords = [
            "senha@123",
            "SENHA@123",
            "SenhaForte@",
            "Senha1234",
            "Se@1",
        ]

        for password in invalid_passwords:
            with self.subTest(password=password), self.assertRaises(ValidationError):
                password_validation.validate_password(password)
