from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from .models import DUPLICADO, Paciente
from .validators import normalizar_cpf


User = get_user_model()


def dados_paciente(**alteracoes):
    dados = {
        "nome_completo": "Pessoa de Teste",
        "cpf": "529.982.247-25",
        "data_nascimento": "1990-05-21",
        "telefone": "(11) 99999-1234",
        "email": "",
    }

    dados.update(alteracoes)
    return dados


class CPFTests(SimpleTestCase):
    def test_aceita_cpf_com_e_sem_mascara(self):
        for cpf in (
            "529.982.247-25",
            "52998224725",
            " 52998224725 ",
        ):
            with self.subTest(cpf=cpf):
                self.assertEqual(
                    normalizar_cpf(cpf),
                    "52998224725",
                )

    def test_preserva_zero_inicial(self):
        self.assertEqual(
            normalizar_cpf("012.345.678-90"),
            "01234567890",
        )

    def test_rejeita_digitos_verificadores_e_formatos_invalidos(self):
        valores = [
            "52998224724",
            "52998224735",
            "123",
            "",
            "529982247250",
            "abc52998224725",
            "529-982-247.25",
            "５２９９８２２４７２５",
        ]

        valores.extend(
            str(i) * 11
            for i in range(10)
        )

        for cpf in valores:
            with self.subTest(cpf=cpf), self.assertRaises(ValidationError):
                normalizar_cpf(cpf)


class PacientesApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario_teste",
            name="Usuário Teste",
            password="senha_teste_123",
            role=User.Role.RECEPTIONIST,
        )

        self.create_url = reverse("pacientes:create")
        self.search_url = reverse("pacientes:buscar")

    def autenticar(self):
        self.client.force_authenticate(user=self.user)

    def test_usuario_autenticado_pode_cadastrar(self):
        self.autenticar()

        response = self.client.post(
            self.create_url,
            dados_paciente(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        paciente = Paciente.objects.get()

        self.assertEqual(
            paciente.nome_completo,
            "Pessoa de Teste",
        )
        self.assertEqual(
            paciente.cpf,
            "52998224725",
        )
        self.assertEqual(
            paciente.telefone,
            "11999991234",
        )

    def test_usuario_nao_autenticado_nao_pode_cadastrar(self):
        response = self.client.post(
            self.create_url,
            dados_paciente(),
            format="json",
        )

        self.assertIn(
            response.status_code,
            {
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            },
        )

        self.assertEqual(
            Paciente.objects.count(),
            0,
        )

    def test_campos_obrigatorios(self):
        self.autenticar()

        for campo in (
            "nome_completo",
            "cpf",
            "data_nascimento",
            "telefone",
        ):
            with self.subTest(campo=campo):
                dados = dados_paciente()
                dados[campo] = ""

                response = self.client.post(
                    self.create_url,
                    dados,
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

                self.assertIn(
                    campo,
                    response.data,
                )

    def test_email_opcional_e_validado(self):
        self.autenticar()

        response = self.client.post(
            self.create_url,
            dados_paciente(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        response = self.client.post(
            self.create_url,
            dados_paciente(
                cpf="111.444.777-35",
                email="pessoa@example.com",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        response = self.client.post(
            self.create_url,
            dados_paciente(
                cpf="123.456.789-09",
                email="email-invalido",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "email",
            response.data,
        )

    def test_nascimento_invalido_ou_futuro(self):
        self.autenticar()

        valores = [
            "2020-02-30",
            "invalida",
            (
                timezone.localdate()
                + timedelta(days=1)
            ).isoformat(),
        ]

        for data in valores:
            with self.subTest(data=data):
                response = self.client.post(
                    self.create_url,
                    dados_paciente(
                        cpf="111.444.777-35",
                        data_nascimento=data,
                    ),
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

                self.assertIn(
                    "data_nascimento",
                    response.data,
                )

    def test_telefone_invalido(self):
        self.autenticar()

        for telefone in (
            "123",
            "abc11999991234",
            "1" * 16,
        ):
            with self.subTest(telefone=telefone):
                response = self.client.post(
                    self.create_url,
                    dados_paciente(
                        cpf="111.444.777-35",
                        telefone=telefone,
                    ),
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

                self.assertIn(
                    "telefone",
                    response.data,
                )

    def test_nome_limpa_espacos(self):
        self.autenticar()

        response = self.client.post(
            self.create_url,
            dados_paciente(
                nome_completo="  Pessoa   de Teste  ",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        paciente = Paciente.objects.get()

        self.assertEqual(
            paciente.nome_completo,
            "Pessoa de Teste",
        )

    def test_cpf_invalido_nao_grava(self):
        self.autenticar()

        response = self.client.post(
            self.create_url,
            dados_paciente(
                cpf="11111111111",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "cpf",
            response.data,
        )

        self.assertEqual(
            Paciente.objects.count(),
            0,
        )

    def test_cpf_duplicado_com_e_sem_mascara(self):
        self.autenticar()

        response = self.client.post(
            self.create_url,
            dados_paciente(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        for cpf in (
            "52998224725",
            "529.982.247-25",
        ):
            with self.subTest(cpf=cpf):
                response = self.client.post(
                    self.create_url,
                    dados_paciente(cpf=cpf),
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

                self.assertIn(
                    "cpf",
                    response.data,
                )

                self.assertIn(
                    DUPLICADO,
                    response.data["cpf"],
                )

        self.assertEqual(
            Paciente.objects.count(),
            1,
        )

    def test_banco_impede_duplicidade(self):
        Paciente.objects.create(
            **dados_paciente()
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            Paciente.objects.create(
                **dados_paciente(
                    cpf="52998224725",
                )
            )

        self.assertEqual(
            Paciente.objects.count(),
            1,
        )

    def test_model_normaliza_e_valida_cpf(self):
        paciente = Paciente(
            **dados_paciente()
        )

        paciente.full_clean()

        self.assertEqual(
            paciente.cpf,
            "52998224725",
        )

        with self.assertRaises(ValidationError):
            Paciente.objects.create(
                **dados_paciente(
                    cpf="11111111111",
                )
            )

    def test_outro_erro_de_integridade_nao_e_disfarcado(self):
        self.autenticar()

        with patch(
            "apps.pacientes.serializers.Paciente.objects.create",
            side_effect=IntegrityError("Outro erro"),
        ):
            with self.assertRaises(IntegrityError):
                self.client.post(
                    self.create_url,
                    dados_paciente(),
                    format="json",
                )


class BuscaPacientesApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario_busca",
            name="Usuário Busca",
            password="senha_teste_123",
            role=User.Role.RECEPTIONIST,
        )

        self.search_url = reverse(
            "pacientes:buscar"
        )

        self.paciente = Paciente.objects.create(
            **dados_paciente()
        )

    def autenticar(self):
        self.client.force_authenticate(user=self.user)

    def test_usuario_nao_autenticado_nao_pode_buscar(self):
        response = self.client.post(
            self.search_url,
            {
                "cpf": "529.982.247-25",
            },
            format="json",
        )

        self.assertIn(
            response.status_code,
            {
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            },
        )

    def test_busca_com_e_sem_mascara(self):
        self.autenticar()

        for cpf in (
            "52998224725",
            "529.982.247-25",
        ):
            with self.subTest(cpf=cpf):
                response = self.client.post(
                    self.search_url,
                    {"cpf": cpf},
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_200_OK,
                )

                self.assertEqual(
                    response.data["nome_completo"],
                    "Pessoa de Teste",
                )

                self.assertEqual(
                    response.data["cpf"],
                    "52998224725",
                )

    def test_paciente_nao_encontrado(self):
        self.autenticar()

        response = self.client.post(
            self.search_url,
            {
                "cpf": "111.444.777-35",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertEqual(
            response.data["detail"],
            "Nenhum paciente encontrado.",
        )

    def test_busca_invalida_ou_vazia(self):
        self.autenticar()

        for cpf in (
            "",
            "00000000000",
            "errado",
        ):
            with self.subTest(cpf=cpf):
                response = self.client.post(
                    self.search_url,
                    {"cpf": cpf},
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

                self.assertIn(
                    "cpf",
                    response.data,
                )

    def test_detalhe_paciente_existente(self):
        self.autenticar()

        url = reverse(
            "pacientes:detail",
            args=[self.paciente.pk],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["nome_completo"],
            "Pessoa de Teste",
        )

        self.assertEqual(
            response.data["cpf"],
            "52998224725",
        )

    def test_detalhe_inexistente(self):
        self.autenticar()

        url = reverse(
            "pacientes:detail",
            args=[999999],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_metodos_nao_previstos(self):
        self.autenticar()

        response = self.client.get(
            self.search_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

        response = self.client.post(
            reverse(
                "pacientes:detail",
                args=[self.paciente.pk],
            ),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )