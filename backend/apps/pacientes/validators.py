import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def normalizar_cpf(valor):
    """Aceita CPF com ou sem máscara e retorna os 11 dígitos."""
    valor = str(valor).strip()

    if not re.fullmatch(
        r"(?:[0-9]{11}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2})",
        valor,
    ):
        raise ValidationError(
            "Informe um CPF com 11 dígitos, com ou sem pontuação.",
            code="invalid",
        )

    cpf = valor.replace(".", "").replace("-", "")

    if len(set(cpf)) == 1:
        raise ValidationError(
            "Informe um CPF válido.",
            code="invalid",
        )

    for tamanho in (9, 10):
        soma = sum(
            int(cpf[i]) * (tamanho + 1 - i)
            for i in range(tamanho)
        )

        digito = (soma * 10 % 11) % 10

        if digito != int(cpf[tamanho]):
            raise ValidationError(
                "Informe um CPF válido.",
                code="invalid",
            )

    return cpf


def validar_cpf(valor):
    normalizar_cpf(valor)


def validar_nascimento(valor):
    if valor > timezone.localdate():
        raise ValidationError(
            "A data de nascimento não pode estar no futuro.",
            code="future",
        )


def validar_telefone(valor):
    if (
        not re.fullmatch(r"\+?[0-9 ()\-.]+", valor)
        or not 10 <= len(re.sub(r"[^0-9]", "", valor)) <= 15
    ):
        raise ValidationError(
            "Informe um telefone com DDD, entre 10 e 15 dígitos.",
            code="invalid",
        )