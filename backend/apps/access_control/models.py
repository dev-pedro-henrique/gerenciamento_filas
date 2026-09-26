from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

username_validator = RegexValidator(
    regex=r"^[a-z0-9._-]+$",
    message="Use apenas letras minúsculas, números, ponto, hífen ou sublinhado.",
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username: str, name: str, password: str | None = None, **extra_fields):
        if not username:
            raise ValueError("O nome de usuário é obrigatório.")
        if not name:
            raise ValueError("O nome completo é obrigatório.")
        user = self.model(username=username.strip().lower(), name=name.strip(), **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, name: str, password: str, **extra_fields):
        extra_fields.setdefault("role", User.Role.MANAGER)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("role") != User.Role.MANAGER:
            raise ValueError("Uma conta administrativa deve possuir o perfil de gestor.")
        if not extra_fields.get("is_staff") or not extra_fields.get("is_superuser"):
            raise ValueError("Uma conta administrativa deve ter privilégios administrativos.")
        return self.create_user(username, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        MANAGER = "MANAGER", "Gestor"
        RECEPTIONIST = "RECEPTIONIST", "Recepção"

    username = models.CharField(
        "nome de usuário", max_length=50, unique=True, validators=[username_validator]
    )
    name = models.CharField("nome completo", max_length=150)
    role = models.CharField("perfil", max_length=20, choices=Role.choices)
    is_active = models.BooleanField("ativo", default=True)
    is_staff = models.BooleanField("acesso administrativo", default=False)
    date_joined = models.DateTimeField("data de cadastro", default=timezone.now)
    active_session_key = models.CharField(max_length=40, blank=True, default="")

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "usuário interno"
        verbose_name_plural = "usuários internos"
        ordering = ["name", "username"]

    def __str__(self) -> str:
        return f"{self.name} ({self.username})"

    def save(self, *args, **kwargs):
        self.username = self.username.strip().lower()
        if self.is_superuser:
            self.role = self.Role.MANAGER
            self.is_staff = True
        super().save(*args, **kwargs)


class LoginAttempt(models.Model):
    username = models.CharField(max_length=50, unique=True)
    failed_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "tentativa de login"
        verbose_name_plural = "tentativas de login"

    def __str__(self) -> str:
        return self.username
