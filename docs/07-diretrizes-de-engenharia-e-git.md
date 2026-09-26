# Diretrizes de engenharia e Git

Estas diretrizes registram o padrão desejado para quando a implementação for autorizada. Elas não definem ainda a arquitetura concreta.

## Princípios de desenvolvimento

- clareza e simplicidade antes de abstrações prematuras;
- regras de negócio explícitas e centralizadas;
- separação entre domínio, aplicação, persistência, interface HTTP e apresentação;
- validação e autorização no backend como fonte de verdade;
- frontend responsável pela experiência, não pela segurança do dado;
- baixo acoplamento entre autenticação interna e acesso do paciente;
- privacidade e menor privilégio por padrão;
- falhas explícitas e observáveis, sem vazamento de dados;
- testes orientados a risco e critérios de aceitação;
- documentação atualizada no mesmo conjunto de mudanças.

## Python e Django

- seguir PEP 8, tipagem onde trouxer clareza e nomes orientados ao domínio;
- adotar o modelo de usuário adequado desde a primeira migração, evitando troca tardia;
- manter views/controladores finos e regras relevantes em serviços ou objetos de domínio apropriados;
- usar recursos consolidados do Django para senha, sessão, CSRF, validação e permissões, salvo motivo documentado;
- nunca implementar armazenamento ou comparação própria de senha;
- usar migrações pequenas, revisáveis e reversíveis quando possível;
- evitar sinais para fluxos de negócio centrais quando dependências explícitas forem mais claras;
- consultas devem evitar N+1 e ser medidas antes de otimizações complexas;
- logs não devem conter senha, token, CPF completo, telefone ou dados clínicos.

## React

- componentes pequenos com responsabilidades claras;
- estado remoto separado do estado puramente visual;
- rotas e navegação por capacidade, mantendo a autorização real no backend;
- formulários acessíveis, mensagens úteis e foco controlado em erros;
- estados de carregamento, vazio, erro e sessão expirada definidos;
- não persistir segredo de autenticação em local inadequado por conveniência;
- página pública do paciente separada conceitualmente da área interna.

## API e contratos

- contratos previsíveis e versionáveis;
- respostas de erro consistentes sem detalhes internos;
- operações críticas idempotentes ou protegidas contra repetição quando aplicável;
- controle de concorrência para impedir chamada duplicada e sobrescrita silenciosa;
- datas e horários armazenados e comparados de forma inequívoca, com apresentação no fuso da clínica;
- paginação, filtros e ordenação definidos no contrato quando necessários.

## Banco de dados

- integridade também garantida por constraints, não apenas pela interface;
- CPF normalizado e único quando presente em cadastro completo, respeitando a regra futura de provisório;
- índices guiados por buscas reais;
- cadastro do paciente separado de entrada, atendimento, auditoria e token;
- exclusão e anonimização desenhadas junto com retenção e backup;
- transações para mudanças que alterem fila, chamada, capacidade ou múltiplos registros correlatos.

## Segurança e privacidade

- menor privilégio;
- negar por padrão;
- proteção contra força bruta, fixação e roubo de sessão a definir tecnicamente;
- segredos somente em configuração segura, nunca no repositório;
- dependências atualizadas e verificadas;
- dados pessoais minimizados em tela, API, log, exportação e backup;
- ameaças de enumeração, IDOR e acesso por link testadas explicitamente;
- eventos relevantes auditáveis sem registrar conteúdo sensível desnecessário.

## Estratégia de testes

- testes unitários para regras puras;
- testes de integração para banco, autenticação, autorização e transações;
- testes de contrato entre frontend e backend;
- testes de fluxo para critérios de aceitação críticos;
- testes negativos de permissão com acesso direto à API;
- testes de concorrência nas operações de chamada e alteração da fila;
- testes de acessibilidade e navegação por teclado nas telas principais.

## Git e colaboração

### Commits

Commits devem ser pequenos, coesos, compiláveis/testáveis quando houver código e escritos no imperativo. Usar Conventional Commits:

- `feat(auth): adiciona encerramento manual de sessão`
- `fix(auth): impede acesso da recepção às configurações`
- `test(auth): cobre expiração por inatividade`
- `docs(requirements): registra política de recuperação`
- `refactor(auth): separa política de permissão do controlador`
- `chore: configura ferramentas de qualidade`

Evitar commits genéricos como `ajustes`, `mudanças` ou grandes lotes com assuntos independentes.

### Branches

Até a equipe decidir outro padrão, proposta:

- `feat/pb01-login-sessao`
- `feat/pb01-autorizacao-perfis`
- `test/pb01-permissoes`
- `docs/regras-autenticacao`

Uma branch deve corresponder a uma unidade revisável. A estratégia final de branches e integração deve ser acordada antes do primeiro desenvolvimento em paralelo.

### Pull requests e revisão

- explicar problema, solução, requisitos atendidos e como testar;
- manter escopo pequeno;
- exigir revisão de outro integrante conforme a definição de concluído;
- não aprovar com teste crítico falhando ou pendência de segurança conhecida;
- anexar evidência de telas ou contratos quando isso facilitar a revisão;
- registrar decisão arquitetural relevante em documento próprio no futuro.

## Qualidade antes da integração

Quando houver implementação, cada mudança deverá passar pelas verificações configuradas do projeto: formatação, lint, análise estática, testes e revisão de migrações. As ferramentas concretas serão escolhidas ao definir a estrutura técnica, sem instalar ou configurar nada nesta fase.

