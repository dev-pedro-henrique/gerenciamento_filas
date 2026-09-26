from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, Throttled

from .models import LoginAttempt, User

INVALID_CREDENTIALS_MESSAGE = "Nome de usuário ou senha inválidos."
LOCKED_MESSAGE = "Acesso temporariamente bloqueado. Tente novamente em alguns minutos."


class InvalidCredentials(APIException):
    status_code = 401
    default_detail = INVALID_CREDENTIALS_MESSAGE
    default_code = "invalid_credentials"


def authenticate_user(request, username: str, password: str) -> User:
    normalized_username = username.strip().lower()
    error: APIException | None = None
    user: User | None = None

    with transaction.atomic():
        attempt, _ = LoginAttempt.objects.select_for_update().get_or_create(
            username=normalized_username
        )
        now = timezone.now()

        if attempt.locked_until and attempt.locked_until > now:
            wait_seconds = max(1, int((attempt.locked_until - now).total_seconds()))
            error = Throttled(wait=wait_seconds, detail=LOCKED_MESSAGE)
        else:
            if attempt.locked_until:
                attempt.failed_attempts = 0
                attempt.locked_until = None

            user = authenticate(request=request, username=normalized_username, password=password)
            if user is None:
                attempt.failed_attempts += 1
                if attempt.failed_attempts >= settings.LOGIN_FAILURE_LIMIT:
                    attempt.locked_until = now + timedelta(seconds=settings.LOGIN_LOCKOUT_SECONDS)
                attempt.save(update_fields=["failed_attempts", "locked_until", "updated_at"])
                error = InvalidCredentials()
            else:
                attempt.delete()

    if error:
        raise error
    if user is None:
        raise InvalidCredentials()
    return user


@transaction.atomic
def start_single_session(request, user: User) -> None:
    if user.active_session_key:
        Session.objects.filter(session_key=user.active_session_key).delete()

    login(request, user)
    if request.session.session_key is None:
        request.session.save()

    user.active_session_key = request.session.session_key or ""
    user.save(update_fields=["active_session_key", "last_login"])


@transaction.atomic
def end_current_session(request) -> None:
    if request.user.is_authenticated:
        session_key = request.session.session_key or ""
        User.objects.filter(
            pk=request.user.pk,
            active_session_key=session_key,
        ).update(active_session_key="")
    logout(request)


def terminate_user_session(user: User) -> None:
    if user.active_session_key:
        Session.objects.filter(session_key=user.active_session_key).delete()
        user.active_session_key = ""
        user.save(update_fields=["active_session_key"])
