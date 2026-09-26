from getpass import getpass

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from apps.access_control.models import User
from apps.access_control.services import terminate_user_session


class Command(BaseCommand):
    help = "Redefine com segurança a senha de um gestor e encerra sua sessão ativa."

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, *args, **options):
        username = options["username"].strip().lower()
        try:
            manager = User.objects.get(username=username, role=User.Role.MANAGER)
        except User.DoesNotExist as error:
            raise CommandError("Gestor não encontrado.") from error

        password = getpass("Nova senha: ")
        confirmation = getpass("Confirme a nova senha: ")
        if password != confirmation:
            raise CommandError("As senhas não coincidem.")

        try:
            password_validation.validate_password(password, manager)
        except ValidationError as error:
            raise CommandError("A senha não atende à política de segurança.") from error

        manager.set_password(password)
        manager.save(update_fields=["password"])
        terminate_user_session(manager)
        self.stdout.write(self.style.SUCCESS("Senha do gestor redefinida com segurança."))
