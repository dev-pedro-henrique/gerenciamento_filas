# Autenticação, autorização e acessos

Este documento aprofunda o item `PB01`, sem transformar decisões técnicas ainda não tomadas em regras confirmadas.

## Escopo da implementação atual

Esta entrega inclui:

- login por nome de usuário e senha;
- sessão interna única, expiração por inatividade e logout;
- autorização dos perfis gestor e recepção;
- cadastro, ativação, desativação e alteração de recepcionistas somente pelo gestor;
- recuperação assistida da conta do gestor por comando administrativo seguro;
- testes de autenticação, sessão, senha, bloqueio e permissões.

Esta entrega não inclui cadastro ou localização de pacientes, link do paciente, filas, serviços, relatórios ou atendimento. As referências a esses módulos neste documento apenas definem fronteiras para integração futura.

## Fronteiras do problema

Há dois mecanismos diferentes e eles não devem ser confundidos:

1. **Autenticação interna:** recepcionistas e gestor comprovam identidade com credenciais próprias para entrar na área operacional.
2. **Acesso individual do paciente:** o paciente não cria conta nem faz login no MVP; um código aleatório no link concede acesso restrito a uma única participação na fila.

O segundo mecanismo é uma credencial de posse limitada, embora não seja uma conta. Ele exige proteção equivalente ao impacto de alguém obter o link.

## Requisitos confirmados

- **AUT-RF-001:** permitir login de usuário interno válido com usuário e senha próprios.
- **AUT-RF-002:** recusar credenciais inválidas sem conceder sessão.
- **AUT-RF-003:** reconhecer os perfis `RECEPCAO` e `GESTOR`.
- **AUT-RF-004:** restringir cada função no servidor conforme o perfil, independentemente do que a interface esconder ou mostrar.
- **AUT-RF-005:** encerrar a sessão após 15 minutos sem uso.
- **AUT-RF-006:** oferecer saída manual.
- **AUT-RF-007:** permitir recuperação de acesso confirmada pelo gestor.
- **AUT-RF-008:** impedir o uso de contas compartilhadas.
- **AUT-RF-009:** permitir navegação compatível com o perfil autenticado.
- **AUT-RF-010:** bloquear acesso da recepção a configurações exclusivas do gestor.
- **AUT-RF-011:** gerar, em etapa posterior do MVP, acesso aleatório e individual para cada entrada do paciente.
- **AUT-RF-012:** garantir que o link do paciente não exponha outra pessoa nem permita acesso à área interna.
- **AUT-RF-013:** permitir somente ao gestor criar, ativar, desativar e alterar o perfil de contas internas.
- **AUT-RF-014:** autenticar contas internas exclusivamente por nome de usuário e senha.
- **AUT-RF-015:** bloquear temporariamente novas tentativas após cinco falhas consecutivas de autenticação.
- **AUT-RF-016:** impedir duas sessões simultâneas para a mesma conta, invalidando a sessão anterior após novo login válido.

## Regras de negócio de acesso

- **AUT-RN-001:** cada pessoa interna deve ser representada por uma conta identificável; não existe conta genérica de recepção.
- **AUT-RN-002:** estar autenticado não basta: toda operação protegida exige autorização correspondente ao papel.
- **AUT-RN-003:** recepcionistas podem operar a fila e os cadastros necessários, mas não alterar configurações exclusivas, corrigir manualmente a ordem nem executar outras ações reservadas ao gestor.
- **AUT-RN-004:** ações críticas devem ser atribuíveis ao usuário real que as executou.
- **AUT-RN-005:** após logout ou expiração, requisições protegidas não podem continuar válidas.
- **AUT-RN-006:** a recuperação não pode contornar a confirmação do gestor. O procedimento alternativo para recuperar a conta do próprio gestor ainda está pendente.
- **AUT-RN-007:** o paciente vê somente posição, pessoas à frente, faixa de espera e status da sua entrada; informações clínicas e identidades de terceiros nunca são retornadas.
- **AUT-RN-008:** autenticação em dois fatores não pertence ao MVP.
- **AUT-RN-009:** a senha possui no mínimo oito caracteres, incluindo letra maiúscula, letra minúscula, número e caractere especial.
- **AUT-RN-010:** após cinco tentativas inválidas, a conta fica temporariamente bloqueada por 15 minutos. O prazo é uma decisão técnica inicial revisável.
- **AUT-RN-011:** a identificação de login é o nome de usuário; e-mail não substitui o identificador.
- **AUT-RN-012:** somente o gestor administra contas, incluindo perfil e estado ativo.
- **AUT-RN-013:** o gestor pode conceder à recepção acesso limitado a histórico e relatórios conforme capacidades que serão refinadas com esses módulos.
- **AUT-RN-014:** o link do paciente expira quando o atendimento é concluído.
- **AUT-RN-015:** a posse de um link válido basta para solicitar cancelamento, sem confirmação adicional.

## Matriz mínima de autorização

Legenda: `P` permitido, `—` não permitido, `N/A` não se aplica ao ator.

| Capacidade | Recepção | Gestor | Paciente por link |
|---|:---:|:---:|:---:|
| Entrar na área interna | P | P | N/A |
| Cadastrar/localizar paciente | P | P | N/A |
| Operar entrada, chamada, início, ausência, cancelamento e conclusão | P | P | N/A |
| Consultar configuração operacional | P | P | N/A |
| Alterar serviços, horários, capacidade, tolerâncias e mensagens | — | P | N/A |
| Corrigir manualmente a ordem | — | P | N/A |
| Confirmar exclusão, reabertura ou alteração do horário original | — | P | N/A |
| Consultar histórico e relatórios | — | P | N/A |
| Consultar a própria espera | N/A | N/A | P |
| Solicitar cancelamento da própria entrada | N/A | N/A | P |
| Acessar outra entrada usando o link recebido | N/A | N/A | — |

A tabela deverá ser refinada quando a clínica definir se a recepção pode consultar algum subconjunto de histórico ou relatórios.

## Ciclos conceituais

### Sessão interna

1. Usuário informa identificador e senha.
2. O sistema valida as credenciais e o estado da conta.
3. Em caso de sucesso, cria uma sessão vinculada ao usuário e ao perfil.
4. Cada requisição protegida valida sessão e permissão.
5. Atividade válida renova ou registra a janela de inatividade, conforme decisão técnica futura.
6. Após 15 minutos sem uso, a sessão expira.
7. Logout manual invalida a sessão no servidor.

### Recuperação de acesso

1. Usuário informa que perdeu o acesso.
2. O gestor confirma a identidade por procedimento administrativo ainda a definir.
3. O sistema ou o gestor inicia uma redefinição limitada e auditável.
4. O usuário define nova senha e sessões anteriores são invalidadas.

Para a conta do próprio gestor, a equipe técnica realizará recuperação assistida por comando administrativo do Django. A senha nunca será escrita em texto puro nem alterada por SQL manual; o comando aplicará o hash seguro e invalidará as sessões existentes.

### Link individual do paciente

1. Uma entrada na fila é criada.
2. É gerado um código aleatório não previsível e vinculado somente àquela entrada.
3. A recepção envia o link manualmente.
4. A página consulta apenas os dados públicos permitidos daquela entrada.
5. Cancelamento exige confirmação e produz evento auditável.
6. O link deixa de conceder acesso quando o atendimento é concluído.

## Critérios de aceitação da Sprint 1

- **AUT-CA-001:** dado um usuário interno ativo e senha correta, quando ele autentica, então entra na área compatível com o seu perfil.
- **AUT-CA-002:** dada uma senha incorreta, quando ocorre a tentativa, então o acesso é recusado e nenhuma sessão autenticada é criada.
- **AUT-CA-003:** dada uma conta de recepção, quando tenta acessar configuração exclusiva do gestor, então a operação é negada inclusive no backend.
- **AUT-CA-004:** dada uma conta de gestor, quando acessa configurações autorizadas, então a operação é permitida.
- **AUT-CA-005:** dada uma sessão sem atividade por 15 minutos, quando ocorre nova tentativa de uso, então o sistema exige nova autenticação.
- **AUT-CA-006:** dada uma sessão ativa, quando o usuário executa logout, então as operações protegidas subsequentes são recusadas.
- **AUT-CA-007:** dados dois profissionais, quando ambos usam o sistema, então cada ação auditável é atribuída à conta correta.
- **AUT-CA-008:** dado um usuário autenticado, quando tenta chamar uma função apenas escondida na interface, então o backend ainda aplica a autorização e recusa o acesso.
- **AUT-CA-009:** dadas cinco senhas incorretas consecutivas, quando ocorre nova tentativa dentro de 15 minutos, então o acesso permanece bloqueado mesmo com a senha correta.
- **AUT-CA-010:** dada uma sessão já ativa, quando a mesma conta realiza novo login válido, então a sessão anterior deixa de acessar recursos protegidos.
- **AUT-CA-011:** dada uma conta de recepção, quando tenta criar, desativar ou alterar outra conta, então a operação é recusada.
- **AUT-CA-012:** dada uma senha sem algum dos grupos obrigatórios, quando o gestor cria ou redefine uma conta, então a senha é recusada com orientação objetiva.

Os critérios sobre link do paciente pertencem principalmente à Sprint 4 (`PB13`), mas sua fronteira deve ser considerada desde a modelagem inicial para não transformar paciente em usuário interno por engano.

## Esqueleto funcional futuro, sem implementação

### Backend

- módulo de identidade e contas internas;
- serviço de autenticação e encerramento de sessão;
- políticas de autorização por capacidade ou papel;
- fluxo administrativo de criação, ativação, desativação e recuperação;
- auditoria de eventos relevantes;
- mecanismo separado de códigos de acesso do paciente.

### Frontend

- tela de login;
- tratamento neutro de erro de credenciais;
- navegação e rotas conforme permissões;
- aviso e redirecionamento por expiração de sessão;
- ação de logout claramente disponível;
- fluxo de recuperação conforme definição futura;
- página pública do paciente isolada da aplicação interna.

### Testes esperados

- credenciais válidas e inválidas;
- sessão criada, expirada e encerrada;
- autorização positiva e negativa por operação;
- tentativa de contornar restrição diretamente pela API;
- conta inativa ou desativada;
- concorrência entre sessões e atribuição de auditoria;
- não exposição de dados em erros, logs ou respostas;
- isolamento entre dois links de pacientes, quando `PB13` for implementado.

## Riscos prioritários

- autorização aplicada apenas no frontend;
- contas genéricas impedindo auditoria;
- sessão continuar válida após logout ou troca de senha;
- recuperação de senha sem prova administrativa suficiente;
- mensagens de login revelarem se uma conta existe;
- código de paciente curto, previsível, reutilizado ou sem expiração;
- dados pessoais em URL, logs, notificações ou cache compartilhado;
- confusão entre perfil interno e paciente.

## Pendências específicas

Continuam abertas apenas decisões que dependem dos módulos futuros de histórico e relatórios. As definições de login, gestão de contas, senha, bloqueio, sessão única e link do paciente foram confirmadas em 25 de setembro de 2026.
