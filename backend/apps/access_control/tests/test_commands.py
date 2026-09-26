from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from .factories import create_manager


class ResetManagerPasswordCommandTests(TestCase):
    @patch(
        "apps.access_control.management.commands.reset_manager_password.getpass",
        side_effect=["NovaSenha@2", "NovaSenha@2"],
    )
    def test_resets_password_and_invalidates_session(self, _mocked_getpass):
        manager = create_manager(active_session_key="old-session")
        output = StringIO()

        call_command("reset_manager_password", manager.username, stdout=output)

        manager.refresh_from_db()
        self.assertTrue(manager.check_password("NovaSenha@2"))
        self.assertEqual(manager.active_session_key, "")
        self.assertIn("redefinida", output.getvalue())
