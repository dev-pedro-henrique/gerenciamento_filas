# Backlog, cronograma e Sprint 1

## Priorização do produto

Todos os itens `PB01` a `PB18` foram classificados como “deve ter” no documento original. Os itens posteriores ao MVP são:

- `PB19` cadastro pelo paciente — deveria ter;
- `PB20` WhatsApp automático — poderia ter;
- `PB21` relatórios avançados — deveria ter;
- `PB22` integrações externas — poderia ter;
- `PB23` autenticação em dois fatores — poderia ter;
- `PB24` várias unidades — poderia ter.

## Cronograma macro original

| Sprint | Semanas | Itens | Entrega | Pontos |
|---|---:|---|---|---:|
| 1 | 1–2 | PB01, PB02, PB03 | Acesso, configuração inicial e cadastro | 18 |
| 2 | 3–4 | PB05, PB06, PB08 | Filas, entrada ordenada e painel | 21 |
| 3 | 5–6 | PB07, PB09, PB10, PB12 | Prioridade, atendimento, ausências e correção | 23 |
| 4 | 7–8 | PB13, PB14, PB15 | Link, posição, estimativa e avisos | 18 |
| 5 | 9–10 | PB04, PB11, PB16, PB18 | Casos especiais, capacidade, privacidade, auditoria e contingência | 24 |
| 6 | 11–12 | PB17 e estabilização | Relatório, integração, correções e piloto | 5 mais reserva |

## Objetivo da Sprint 1

Disponibilizar a base do sistema com acesso controlado, configuração inicial da clínica e cadastro de pacientes. A duração prevista é de duas semanas, com 60 horas de capacidade, 56 comprometidas e quatro reservadas.

### Recorte deste trabalho

Apesar de a Sprint 1 do grupo conter `PB01`, `PB02` e `PB03`, a implementação sob responsabilidade atual cobre apenas `PB01`: login, sessão, autorização e cadastro/gestão de recepcionistas pelo gestor. `PB02` e `PB03`, inclusive todo cadastro de pacientes, pertencem a outros integrantes e não serão implementados neste conjunto de commits.

## Itens e critérios da Sprint 1

### PB01 Autenticação e perfis — 5 pontos

- usuário válido entra;
- senha inválida é recusada;
- recepção não acessa configurações exclusivas do gestor.

### PB02 Configuração operacional — 5 pontos

- gestor cria e edita serviço, duração, horário e postos ativos;
- recepção apenas consulta esses dados.

### PB03 Cadastro e localização — 8 pontos

- recepção cadastra e localiza paciente;
- CPF inválido ou repetido é recusado;
- e-mail é opcional;
- nenhum dado clínico é solicitado.

## Tarefas originais da Sprint 1

| ID | Tarefa | Responsáveis registrados | Estimativa |
|---|---|---|---:|
| T01 | Revisar histórias, critérios e dados obrigatórios | Todos | 4 h |
| T02 | Preparar repositório, projeto e ambiente | Caio e Pedro | 6 h |
| T03 | Modelar usuários, perfis, serviços e pacientes e criar migrações | Luiz e Ruan | 8 h |
| T04 | Implementar login, sessão e autorização | Pedro e Edinaldo | 8 h |
| T05 | Criar tela de login e navegação por perfil | Caio e Edinaldo | 6 h |
| T06 | Implementar serviços, horários e postos | Ruan e Luiz | 8 h |
| T07 | Implementar paciente, CPF, busca e duplicidade | Caio, Pedro e Luiz | 10 h |
| T08 | Criar testes de validações, permissões e fluxos | Edinaldo e Ruan | 6 h |
| T09 | Revisar, documentar e preparar demonstração | Todos | 4 h |

O solicitante informou que atualmente é responsável pela autenticação, mas sua identidade e a divisão atual do grupo não foram inferidas dos documentos.

## Definição de concluído fornecida

- critérios de aceitação demonstrados;
- revisão por outro integrante;
- testes automatizados e manuais executados;
- nenhum defeito crítico ou alto conhecido;
- execução no ambiente de teste acordado;
- decisões técnicas necessárias registradas.

## Riscos já registrados

- decisão da clínica pendente: tornar configurável quando possível e registrar para validação;
- tempo menor: priorizar `PB01` e `PB03`, reduzindo somente detalhes visuais de `PB02`;
- conflitos de alteração: trabalho em pares, revisão e uma ramificação por item;
- aumento de escopo: não iniciar itens fora de `PB01`, `PB02` e `PB03` na Sprint 1.

## Dependências da autenticação

- `PB01` fornece identidade e autorização para `PB02`, `PB03` e todos os módulos internos futuros.
- O modelo de usuário deve existir antes da auditoria de `PB16`, mesmo que a auditoria completa esteja planejada para a Sprint 5.
- A separação entre conta interna e link do paciente reduz retrabalho quando `PB13` começar.
- Critérios de permissão precisam ser testados no backend e no frontend desde a Sprint 1.
