import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class StrongPasswordValidator:
    message = _(
        "A senha deve ter pelo menos 8 caracteres, com letra maiúscula, letra minúscula, "
        "número e caractere especial."
    )

    def validate(self, password: str, user=None) -> None:
        del user
        rules = (
            len(password) >= 8,
            re.search(r"[A-Z]", password),
            re.search(r"[a-z]", password),
            re.search(r"\d", password),
            re.search(r"[^A-Za-z0-9]", password),
        )
        if not all(rules):
            raise ValidationError(self.message, code="password_not_strong")

    def get_help_text(self) -> str:
        return self.message
