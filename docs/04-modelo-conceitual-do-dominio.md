# Modelo conceitual do domínio

Este mapa organiza os conceitos do negócio. Não define tabelas, classes Django, endpoints ou componentes React.

## Entidades centrais

### Usuário interno

Representa uma pessoa da equipe com credenciais próprias. Possui identidade, estado da conta e um perfil de acesso. Não representa paciente.

### Perfil de acesso

Conjunto de capacidades atribuído ao usuário. Perfis confirmados no MVP: recepção e gestor.

### Sessão autenticada

Representa um acesso interno em andamento, sujeito a logout e expiração após inatividade.

### Paciente

Cadastro civil e de contato reutilizável. Inclui nome, CPF quando completo, data de nascimento, telefone e e-mail opcional. Não contém serviço, posição, diagnóstico ou conteúdo clínico.

### Responsável legal

Pessoa vinculada a um paciente representado, com nome, CPF, telefone e vínculo. A presença do responsável é confirmada na operação, enquanto autorizações formais permanecem fora do sistema.

### Serviço

Tipo operacional de atendimento com nome, duração média, horários e regras de capacidade. Inicialmente: acolhimento inicial e atendimento psicológico.

### Psicólogo

Profissional responsável por atendimentos e por uma fila própria. O primeiro incremento admite um único psicólogo, mas a entidade deve existir de forma independente para permitir novos profissionais futuramente. Psicólogo não é usuário do sistema no MVP.

### Fila

Agrupa entradas vinculadas a um psicólogo responsável. A primeira versão operará uma fila de um único psicólogo, preservando a possibilidade de novas filas quando outros profissionais forem cadastrados.

### Entrada na fila

Evento que liga paciente, fila, serviço, horário confirmado, prioridade, restrição de profissional quando aplicável, posição derivada, estimativa e status. É distinta do cadastro do paciente.

### Prioridade legal

Categoria configurável aplicada à entrada, com motivo geral e autoria do registro. Urgência clínica não é uma categoria dessa entidade.

### Posto de atendimento

Unidade de capacidade ativa ou pausada para um serviço. Abstrai a disponibilidade combinada de profissional e sala no MVP.

### Atendimento

Registra o início e a conclusão ligados a uma entrada. Não é prontuário e não contém conteúdo terapêutico.

### Código de acompanhamento

Credencial aleatória vinculada a uma única entrada, usada para consulta pública restrita e solicitação de cancelamento.

### Evento de auditoria

Registro imutável conceitual de ator, ação, data e hora, objeto afetado, estado anterior, estado novo e justificativa quando exigida.

### Configuração operacional

Agrupa horários, tolerância, mensagens neutras, categorias de prioridade e outros parâmetros que o gestor pode alterar.

### Registro de contingência

Representa a entrada manual posterior à indisponibilidade, preservando o horário original e a origem de contingência.

## Relacionamentos principais

- um usuário interno possui um perfil e pode originar várias sessões e eventos de auditoria;
- um paciente pode ter várias entradas na fila ao longo do tempo;
- um paciente pode estar ligado a um ou mais responsáveis, conforme regra futura de cardinalidade;
- um psicólogo possui sua própria fila operacional;
- uma fila pode organizar entradas de serviços compatíveis com o psicólogo responsável;
- uma entrada pertence a um paciente e a uma fila;
- uma entrada pode receber uma prioridade legal;
- uma entrada possui no máximo um atendimento correspondente e um código de acompanhamento ativo, conforme decisão futura;
- alterações relevantes em entrada, atendimento, configuração ou acesso geram eventos de auditoria.

## Estados conceituais da entrada

Os documentos citam explicitamente estados como aguardando, vez próxima, chamado e encerrado, além dos eventos de início, conclusão, ausência e cancelamento. Uma máquina de estados definitiva ainda precisa ser validada. Esboço proposto:

`AGUARDANDO → VEZ_PROXIMA → CHAMADO → EM_ATENDIMENTO → CONCLUIDO`

Saídas alternativas propostas:

- `AGUARDANDO/VEZ_PROXIMA/CHAMADO → CANCELADO`;
- `CHAMADO → AUSENTE → AGUARDANDO_NO_FINAL`, uma única vez no turno;
- segunda ausência → `ENCERRADO_POR_AUSENCIA`;
- urgência ou exceção → saída operacional genérica a definir.

`VEZ_PROXIMA` pode ser uma apresentação derivada, e não um estado persistido. `ENCERRADO` pode ser um agrupador visual de conclusões, cancelamentos e ausências finais. Essas decisões permanecem abertas.

## Invariantes de domínio

- um CPF completo identifica no máximo um paciente ativo no cadastro;
- uma entrada pertence a exatamente uma fila e um serviço compatível;
- posição e estimativa são derivadas do estado atual, não dados cadastrais do paciente;
- somente uma chamada ativa pode existir para a mesma entrada;
- o segundo retorno por ausência no mesmo turno não é permitido;
- somente gestor altera manualmente ordem e confirma ações críticas definidas;
- nenhuma entidade operacional armazena conteúdo clínico;
- acesso público nunca atravessa a fronteira de uma entrada para outra.
