from apps.access_control.models import User

DEFAULT_PASSWORD = "Senha@123"


def create_manager(**overrides) -> User:
    values = {
        "username": "gestor",
        "name": "Gestor da Clínica",
        "password": DEFAULT_PASSWORD,
        "role": User.Role.MANAGER,
        "is_staff": True,
    }
    values.update(overrides)
    return User.objects.create_user(**values)


def create_receptionist(**overrides) -> User:
    values = {
        "username": "recepcao",
        "name": "Recepcionista da Clínica",
        "password": DEFAULT_PASSWORD,
        "role": User.Role.RECEPTIONIST,
    }
    values.update(overrides)
    return User.objects.create_user(**values)
