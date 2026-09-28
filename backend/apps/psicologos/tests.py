from unittest.mock import patch

from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.access_control.tests.factories import create_manager, create_receptionist

from .models import Fila, Psicologo


class PsicologosApiTests(APITestCase):
    def setUp(self):
        self.manager = create_manager()
        self.url = reverse("psicologos:list-create")

    def autenticar_gestor(self):
        self.client.force_authenticate(user=self.manager)

    def test_gestor_cadastra_psicologo_com_fila_propria(self):
        self.autenticar_gestor()

        response = self.client.post(
            self.url,
            {"nome_completo": "  Ana   Beatriz  "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome_completo"], "Ana Beatriz")
        self.assertTrue(response.data["ativo"])

        psicologo = Psicologo.objects.get()
        fila = Fila.objects.get(psicologo=psicologo)
        self.assertEqual(response.data["fila_id"], fila.id)

    def test_cada_psicologo_recebe_uma_fila_distinta(self):
        self.autenticar_gestor()

        primeira = self.client.post(
            self.url,
            {"nome_completo": "Ana Beatriz"},
            format="json",
        )
        segunda = self.client.post(
            self.url,
            {"nome_completo": "Carlos Eduardo"},
            format="json",
        )

        self.assertNotEqual(primeira.data["fila_id"], segunda.data["fila_id"])
        self.assertEqual(Fila.objects.count(), 2)

    def test_falha_ao_criar_fila_desfaz_cadastro_do_psicologo(self):
        self.autenticar_gestor()

        with patch(
            "apps.psicologos.serializers.Fila.objects.create",
            side_effect=IntegrityError("Falha ao criar fila"),
        ), self.assertRaises(IntegrityError):
            self.client.post(
                self.url,
                {"nome_completo": "Ana Beatriz"},
                format="json",
            )

        self.assertEqual(Psicologo.objects.count(), 0)
        self.assertEqual(Fila.objects.count(), 0)

    def test_gestor_lista_e_edita_sem_recriar_fila(self):
        self.autenticar_gestor()
        criado = self.client.post(
            self.url,
            {"nome_completo": "Ana Beatriz"},
            format="json",
        )

        detalhe = reverse("psicologos:detail", args=[criado.data["id"]])
        response = self.client.patch(
            detalhe,
            {"nome_completo": "Ana Beatriz Souza", "ativo": False},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome_completo"], "Ana Beatriz Souza")
        self.assertFalse(response.data["ativo"])
        self.assertEqual(response.data["fila_id"], criado.data["fila_id"])
        self.assertEqual(Fila.objects.count(), 1)

        listagem = self.client.get(self.url)
        self.assertEqual(listagem.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listagem.data), 1)

    def test_nome_e_obrigatorio(self):
        self.autenticar_gestor()

        response = self.client.post(
            self.url,
            {"nome_completo": "   "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nome_completo", response.data)
        self.assertEqual(Psicologo.objects.count(), 0)
        self.assertEqual(Fila.objects.count(), 0)

    def test_recepcao_nao_administra_psicologos(self):
        recepcionista = create_receptionist()
        self.client.force_authenticate(user=recepcionista)

        response = self.client.post(
            self.url,
            {"nome_completo": "Ana Beatriz"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Psicologo.objects.count(), 0)

    def test_usuario_nao_autenticado_nao_acessa(self):
        response = self.client.get(self.url)

        self.assertIn(
            response.status_code,
            {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN},
        )
