# Implementação da autenticação

## Escopo entregue

A implementação cobre apenas identidade e acesso de usuários internos. O gestor administra contas de recepcionistas; a recepção autentica e recebe acesso aos módulos que serão integrados posteriormente. Não existem modelos ou endpoints de paciente neste incremento.

## Organização do monólito

```text
backend/
  apps/access_control/   identidade, sessão, autorização e API
  config/                configuração global e rotas
frontend/
  src/api/               cliente HTTP e CSRF
  src/auth/              contexto de sessão
  src/components/        layout e componentes reutilizáveis
  src/pages/             login, início e recepcionistas
```

Novos módulos Django devem ser adicionados em `backend/apps/`. Eles podem depender da identidade por meio de `settings.AUTH_USER_MODEL`, `get_user_model()` ou relacionamentos configuráveis, sem importar implementações concretas desnecessariamente.

## Modelo de usuário

`User` é o modelo de autenticação desde a migração inicial e contém:

- `username`: identificador único normalizado em minúsculas;
- `name`: nome completo;
- `role`: `MANAGER` ou `RECEPTIONIST`;
- `is_active`: controla se a conta pode autenticar;
- `is_staff` e `is_superuser`: reservados à administração Django;
- `active_session_key`: identifica a única sessão aceita para a conta;
- datas e permissões padrão do Django.

O cadastro público de usuários não existe. A API de equipe sempre força o perfil `RECEPTIONIST`, mesmo que outro papel seja enviado no corpo.

## Contratos da API

Todas as rotas usam JSON, sessão por cookie e proteção CSRF. Requisições mutáveis devem enviar `X-CSRFToken`.

| Método | Rota | Acesso | Finalidade |
|---|---|---|---|
| GET | `/api/auth/csrf/` | Público | Inicializa o cookie CSRF. |
| POST | `/api/auth/login/` | Público com CSRF | Autentica e substitui qualquer sessão anterior. |
| POST | `/api/auth/logout/` | Autenticado | Encerra a sessão atual. |
| GET | `/api/auth/me/` | Autenticado | Retorna usuário e perfil atuais. |
| GET | `/api/staff/receptionists/` | Gestor | Lista contas de recepção. |
| POST | `/api/staff/receptionists/` | Gestor | Cria conta de recepção. |
| GET | `/api/staff/receptionists/{id}/` | Gestor | Consulta uma conta de recepção. |
| PATCH | `/api/staff/receptionists/{id}/` | Gestor | Atualiza dados, senha ou estado. |
| POST | `/api/staff/receptionists/{id}/reset-password/` | Gestor | Redefine senha e encerra a sessão da conta. |

## Respostas e estados relevantes

- `200`: leitura, login ou atualização concluída;
- `201`: recepcionista criada;
- `204`: logout ou redefinição concluída sem corpo;
- `400`: dados inválidos, senha fraca ou nome de usuário duplicado;
- `401`: credenciais de login inválidas;
- `403`: ausência de sessão, CSRF inválido ou papel sem permissão;
- `429`: conta temporariamente bloqueada após tentativas inválidas.

O frontend trata perda de sessão e retorna automaticamente ao login. Restrições de rota no React existem para experiência do usuário; toda autorização efetiva é repetida no Django.

## Segurança aplicada

- hash e autenticação nativos do Django;
- política de senha por validadores;
- mensagem neutra para credenciais inválidas;
- bloqueio transacional após cinco falhas;
- cookie de sessão `HttpOnly` e `SameSite=Lax`;
- CSRF obrigatório inclusive no login;
- invalidação da sessão anterior em novo login;
- desativação ou troca de senha encerra sessão ativa;
- segredo e credenciais do banco fora do Git;
- nenhuma senha, CPF ou dado clínico em logs da aplicação.

O bloqueio usa 15 minutos como decisão técnica inicial. A tabela `LoginAttempt` foi separada do usuário para produzir a mesma resposta para nomes existentes e inexistentes.

## Integração com módulos futuros

- use `request.user` para autoria e auditoria;
- verifique capacidades no backend, nunca apenas o valor escondido na interface;
- adicione links laterais por perfil sem alterar o mecanismo de sessão;
- não reutilize `User` para paciente ou psicólogo; são conceitos distintos;
- psicólogos poderão possuir filas futuras sem receber conta de acesso no MVP;
- cadastro de pacientes deve ser implementado em módulo próprio por outro integrante.

## Testes e qualidade

O backend cobre:

- criação e normalização de usuário;
- política de senha;
- CSRF no login;
- credenciais válidas e inválidas;
- bloqueio e desbloqueio temporal;
- sessão única e logout;
- autorização do gestor;
- criação, desativação e redefinição de recepcionistas;
- comando de recuperação do gestor.

O frontend passa por TypeScript estrito, ESLint e build de produção. O fluxo visual foi inspecionado em navegador nas larguras desktop e móvel.

### Estado da validação de banco

O driver MySQL e o `compose.yaml` foram validados. A execução real das migrações no MySQL deve ser repetida quando o Docker Desktop estiver ativo; durante esta sessão o daemon estava desligado e não havia serviço MySQL instalado. A suíte automatizada utiliza explicitamente `DJANGO_USE_SQLITE=true` para permanecer isolada e reproduzível.
