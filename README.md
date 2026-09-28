# Sistema de Gerenciamento de Filas para Clínica de Psicologia

Projeto acadêmico da disciplina de Projeto Integrador da UNIFACISA. O produto será um sistema de gerenciamento de filas adaptado ao contexto de uma clínica de psicologia. A ideia inicial de uma plataforma SaaS white label não faz parte do escopo atual.

O projeto implementa autenticação e gestão de usuários internos, cadastro de pacientes e cadastro administrativo de psicólogos. Cada psicólogo recebe uma fila individual preparada para a integração do fluxo operacional futuro.

## Documentação do projeto

A documentação viva está em [`docs/`](docs/README.md):

- contexto, objetivos, escopo e jornada;
- requisitos funcionais e não funcionais;
- regras de negócio;
- autenticação, autorização e fronteiras de acesso;
- mapa conceitual de entidades;
- backlog, cronograma e Sprint 1;
- decisões, hipóteses e dúvidas pendentes;
- diretrizes futuras de engenharia, arquitetura e Git.

## Escopo implementado

- login por nome de usuário e senha;
- perfis gestor e recepção;
- uma única sessão ativa por usuário;
- expiração após 15 minutos sem atividade;
- bloqueio por 15 minutos após cinco tentativas inválidas;
- logout e invalidação de sessão;
- cadastro, edição, ativação, desativação e redefinição de senha de recepcionistas pelo gestor;
- cadastro, edição, ativação e desativação de psicólogos pelo gestor;
- criação automática de uma fila individual para cada psicólogo;
- recuperação assistida da senha do gestor por comando administrativo;
- interface responsiva baseada na identidade visual fornecida.

Entradas e operação das filas, serviços e relatórios ainda não foram implementados.

## Tecnologias

- Backend: Python e Django;
- Frontend: React;
- Banco de dados: MySQL.

Versões e dependências estão fixadas em `requirements.txt` e `frontend/package-lock.json`.

## Preparação do ambiente

### 1. Variáveis de ambiente

No PowerShell:

```powershell
Copy-Item .env.example .env
```

O Django e o Docker Compose carregam o arquivo `.env` local. Esse arquivo não deve ser versionado.

### 2. MySQL

Com Docker disponível:

```powershell
docker compose up -d mysql
```

Também é possível usar uma instância MySQL 8.4 já instalada, ajustando as variáveis `MYSQL_*`.
Se o comando não encontrar a API do Docker, inicie o Docker Desktop e execute novamente.

### 3. Backend

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe backend\manage.py migrate
.\.venv\Scripts\python.exe backend\manage.py createsuperuser
.\.venv\Scripts\python.exe backend\manage.py runserver
```

O primeiro superusuário recebe automaticamente o perfil de gestor.

### 4. Frontend

```powershell
npm install --prefix frontend
npm run dev --prefix frontend
```

Aplicação: `http://localhost:5173`

API: `http://127.0.0.1:8000/api/`

## Verificações

```powershell
$env:DJANGO_USE_SQLITE='true'
.\.venv\Scripts\ruff.exe check backend
.\.venv\Scripts\coverage.exe run backend\manage.py test apps.access_control
.\.venv\Scripts\coverage.exe report
npm run typecheck --prefix frontend
npm run lint --prefix frontend
npm run build --prefix frontend
```

O SQLite é usado somente para testes locais automatizados. O ambiente normal permanece configurado para MySQL.

## Recuperação assistida do gestor

```powershell
.\.venv\Scripts\python.exe backend\manage.py reset_manager_password nome_do_usuario
```

O comando solicita a senha sem exibi-la, aplica os validadores do sistema e encerra a sessão anterior.

## Documentação técnica

Consulte [`docs/09-implementacao-da-autenticacao.md`](docs/09-implementacao-da-autenticacao.md) para contratos da API, modelo de acesso e pontos de integração.
