import re

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import DUPLICADO, Paciente
from .validators import (
    normalizar_cpf,
    validar_nascimento,
    validar_telefone,
)


class CPFSerializer(serializers.Serializer):
    cpf = serializers.CharField(
        max_length=14,
        trim_whitespace=True,
    )

    def validate_cpf(self, value):
        try:
            return normalizar_cpf(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                error.messages
            ) from error


class PacienteSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(
        max_length=14,
        trim_whitespace=True,
    )

    class Meta:
        model = Paciente
        fields = [
            "id",
            "nome_completo",
            "cpf",
            "data_nascimento",
            "telefone",
            "email",
        ]
        read_only_fields = ["id"]

    def validate_nome_completo(self, value):
        value = " ".join(value.split())

        if not value:
            raise serializers.ValidationError(
                "Informe o nome completo."
            )

        return value

    def validate_cpf(self, value):
        try:
            cpf = normalizar_cpf(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                error.messages
            ) from error

        if Paciente.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError(DUPLICADO)

        return cpf

    def validate_data_nascimento(self, value):
        try:
            validar_nascimento(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                error.messages
            ) from error

        return value

    def validate_telefone(self, value):
        try:
            validar_telefone(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                error.messages
            ) from error

        return re.sub(r"[^0-9]", "", value)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return Paciente.objects.create(**validated_data)

        except IntegrityError as error:
            if Paciente.objects.filter(
                cpf=validated_data["cpf"]
            ).exists():
                raise serializers.ValidationError(
                    {"cpf": [DUPLICADO]}
                ) from error

            raise