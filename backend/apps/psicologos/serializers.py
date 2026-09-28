from django.db import transaction
from rest_framework import serializers

from .models import Fila, Psicologo


class PsicologoSerializer(serializers.ModelSerializer):
    fila_id = serializers.IntegerField(source="fila.id", read_only=True)

    class Meta:
        model = Psicologo
        fields = ("id", "nome_completo", "ativo", "criado_em", "fila_id")
        read_only_fields = ("id", "criado_em", "fila_id")

    def validate_nome_completo(self, value: str) -> str:
        nome = " ".join(value.split())
        if not nome:
            raise serializers.ValidationError("Informe o nome completo.")
        return nome

    @transaction.atomic
    def create(self, validated_data):
        psicologo = Psicologo.objects.create(**validated_data)
        Fila.objects.create(psicologo=psicologo)
        return psicologo
