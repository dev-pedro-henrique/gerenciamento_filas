# Implementação de psicólogos e filas

## Escopo entregue

Este incremento implementa o cadastro administrativo de psicólogos e cria uma fila individual para cada profissional. Psicólogo continua sendo uma entidade distinta de usuário interno e não recebe credenciais de acesso.

O gerenciamento operacional da fila — entradas de pacientes, ordenação, prioridade, chamada, ausência, atendimento e conclusão — não faz parte deste incremento.

## Modelo

`Psicologo` contém somente os dados mínimos atualmente necessários:

- `nome_completo`;
- `ativo`, para retirar o profissional da operação futura sem apagar seu histórico;
- data de criação.

`Fila` possui uma relação um para um protegida com `Psicologo`. A API cria ambos os registros na mesma transação, garantindo uma fila distinta para cada psicólogo cadastrado pelo fluxo oficial.

Campos profissionais adicionais, como CRP, não foram presumidos porque não constam nas fontes confirmadas. A definição desses campos está registrada em `PEN-016`.

## API

As rotas exigem perfil gestor e usam a sessão interna e a proteção CSRF existentes.

| Método | Rota | Finalidade |
|---|---|---|
| GET | `/api/psicologos/` | Listar psicólogos e o identificador de suas filas. |
| POST | `/api/psicologos/` | Cadastrar psicólogo e criar sua fila. |
| GET | `/api/psicologos/{id}/` | Consultar um psicólogo. |
| PATCH | `/api/psicologos/{id}/` | Alterar nome ou estado ativo. |

Não há exclusão física pela API, preservando o vínculo que será usado pelo histórico operacional.

## Interface

O gestor acessa **Psicólogos** pela navegação interna. A tela permite buscar, cadastrar, editar e ativar ou desativar profissionais, além de exibir o identificador da fila preparada para cada cadastro.
