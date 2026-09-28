from django.db import models


class Psicologo(models.Model):
    nome_completo = models.CharField("nome completo", max_length=200)
    ativo = models.BooleanField("ativo", default=True)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        ordering = ["nome_completo", "id"]
        verbose_name = "psicólogo"
        verbose_name_plural = "psicólogos"

    def __str__(self) -> str:
        return self.nome_completo


class Fila(models.Model):
    psicologo = models.OneToOneField(
        Psicologo,
        on_delete=models.PROTECT,
        related_name="fila",
        verbose_name="psicólogo",
    )
    criada_em = models.DateTimeField("criada em", auto_now_add=True)

    class Meta:
        ordering = ["psicologo__nome_completo"]
        verbose_name = "fila"
        verbose_name_plural = "filas"

    def __str__(self) -> str:
        return f"Fila de {self.psicologo.nome_completo}"
