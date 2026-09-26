# Histórico do projeto

Este registro acompanha a evolução do entendimento, das decisões e das entregas. Ele não substitui o histórico do Git quando o repositório for inicializado.

## 25 de setembro de 2026

### Fase

Descoberta funcional e organização documental, antes da implementação.

### Trabalho realizado

- leitura estrutural e cruzamento do questionário preenchido, da consolidação de perguntas e respostas e do product backlog;
- consolidação da visão, escopo, atores, jornada, requisitos e regras de negócio;
- aprofundamento de autenticação, autorização, sessão, recuperação e acesso do paciente;
- criação do mapa conceitual de entidades e invariantes;
- registro do backlog, cronograma, Sprint 1 e dependências da autenticação;
- separação entre decisões confirmadas, hipóteses e pendências;
- definição das diretrizes futuras de engenharia e versionamento.

### Decisões de organização

- documentação funcional centralizada em `docs/`;
- `AGENTS.md` orienta futuras sessões a consultar a base antes de alterar o projeto;
- identificadores estáveis serão usados para requisitos, regras, decisões e pendências;
- cadastro do paciente e entrada na fila são conceitos separados;
- conta interna e link do paciente são mecanismos de acesso diferentes.

### Estado técnico

- nenhum código de aplicação foi criado;
- nenhum projeto Django ou React foi iniciado;
- nenhum esquema ou migração de banco foi criado;
- nenhuma dependência foi instalada;
- a pasta ainda não é um repositório Git.

### Próximo marco esperado

Validar primeiro as pendências que alteram o comportamento da autenticação. Só depois disso, com autorização explícita, definir arquitetura e iniciar a estrutura técnica da Sprint 1.

## 25 de setembro de 2026 — início da implementação

- autorizado inicialmente o desenvolvimento de login, gestão de contas e cadastro/localização de pacientes;
- definido nome de usuário como identificador de login;
- gestão de contas reservada ao gestor;
- definida política de senha forte, cinco tentativas e bloqueio temporário inicial de 15 minutos;
- definida sessão única por conta;
- recuperação do próprio gestor será assistida pela equipe técnica por comando seguro da aplicação;
- link do paciente expira na conclusão e permite cancelamento sem confirmação adicional;
- primeira versão considera um psicólogo, com modelo extensível para uma fila por profissional;
- referência visual adotada: fundo verde sálvia claro, cartões brancos, bordas suaves, tipografia sóbria e ações em verde escuro.

### Correção de escopo

- o cadastro mencionado pelo responsável é o cadastro de recepcionistas, não de pacientes;
- a entrega atual fica restrita a login, sessão, autorização e gestão de recepcionistas pelo gestor;
- cadastro de pacientes pertence a outro integrante e não deve ser implementado nestes commits.
