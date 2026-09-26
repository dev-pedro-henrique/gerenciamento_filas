from django.db import models

from .validators import (
    normalizar_cpf,
    validar_cpf,
    validar_nascimento,
    validar_telefone,
)


DUPLICADO = (
    "Já existe um paciente cadastrado com este CPF. "
    "Utilize a busca para localizá-lo."
)


class Paciente(models.Model):
    nome_completo = models.CharField(
        "Nome completo",
        max_length=200,
    )

    cpf = models.CharField(
        "CPF",
        max_length=11,
        unique=True,
        validators=[validar_cpf],
        error_messages={
            "unique": DUPLICADO,
        },
    )

    data_nascimento = models.DateField(
        "Data de nascimento",
        validators=[validar_nascimento],
    )

    telefone = models.CharField(
        "Telefone",
        max_length=25,
        validators=[validar_telefone],
    )

    email = models.EmailField(
        "E-mail",
        blank=True,
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo

    def clean_fields(self, exclude=None):
        if not exclude or "cpf" not in exclude:
            self.cpf = normalizar_cpf(self.cpf)

        super().clean_fields(exclude=exclude)

    def save(self, *args, **kwargs):
        self.cpf = normalizar_cpf(self.cpf)
        return super().save(*args, **kwargs)

    @property
    def cpf_formatado(self):
        return (
            f"{self.cpf[:3]}.{self.cpf[3:6]}."
            f"{self.cpf[6:9]}-{self.cpf[9:]}"
        )

    @property
    def telefone_formatado(self):
        if len(self.telefone) in (10, 11) and self.telefone.isdigit():
            return (
                f"({self.telefone[:2]}) "
                f"{self.telefone[2:-4]}-{self.telefone[-4:]}"
            )

        return self.telefone