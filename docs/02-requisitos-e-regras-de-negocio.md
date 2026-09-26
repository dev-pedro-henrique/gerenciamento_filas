# Requisitos e regras de negócio

## Requisitos funcionais

| ID | Requisito | Origem principal |
|---|---|---|
| RF-001 | Permitir acesso individual de profissionais internos e restringir funções conforme o perfil recepção ou gestor. | F01 Q11–14, Q63; PB01 |
| RF-002 | Cadastrar, editar e consultar serviços, duração média, horários, postos ativos, tolerância, mensagens neutras e categorias de prioridade. | F01 Q20, Q22–23, Q53; PB02 |
| RF-003 | Cadastrar e localizar pacientes por dados cadastrais, validando CPF e evitando duplicidade. | F01 Q15–16; PB03 |
| RF-004 | Permitir cadastro provisório e cadastro de responsável legal conforme regras específicas. | F01 Q17–18; PB04 |
| RF-005 | Manter fila vinculada ao psicólogo responsável, começando com um único profissional e permitindo inclusão futura de outros. | Decisão posterior de 25/09/2026; substitui parcialmente F01 Q24 e PB05 |
| RF-006 | Confirmar presença e incluir paciente na fila, preservando o horário correto de entrada. | F01 Q25–26; PB06 |
| RF-007 | Registrar prioridade legal com motivo geral e rastreabilidade. | F01 Q27; PB07 |
| RF-008 | Exibir painel com filas, ordem, paciente, entrada, espera, prioridade, status, capacidade e alertas. | F01 Q49; PB08 |
| RF-009 | Chamar, confirmar retorno, iniciar e concluir atendimento. | F01 Q30; PB09 |
| RF-010 | Registrar cancelamento, desistência, ausência e um retorno ao fim da fila no mesmo turno. | F01 Q31, Q45; PB10 |
| RF-011 | Pausar e retomar postos, recalculando a previsão conforme a capacidade. | F01 Q29; PB11 |
| RF-012 | Permitir somente ao gestor corrigir manualmente a ordem mediante justificativa. | F01 Q28; PB12 |
| RF-013 | Gerar link individual com código aleatório para uma entrada específica na fila. | F01 Q34; PB13 |
| RF-014 | Mostrar ao paciente posição, pessoas à frente, faixa aproximada de espera e status. | F01 Q33–37; PB14 |
| RF-015 | Atualizar a página e destacar aproximação, chamada, mudança relevante, cancelamento e encerramento com linguagem neutra. | F01 Q38–42; PB15 |
| RF-016 | Restringir dados por perfil e registrar ações relevantes com estado anterior e novo. | F01 Q13, Q56; PB16 |
| RF-017 | Consultar indicadores básicos, filtrar por período, serviço e turno e exportar CSV. | F01 Q54–55; PB17 |
| RF-018 | Suportar backup diário e posterior lançamento de registros de contingência com o horário original. | F01 Q47, Q65; PB18 |

## Regras de negócio

### Cadastro e identificação

- **RN-001:** no cadastro completo, nome completo, CPF, data de nascimento e telefone são obrigatórios; e-mail é opcional.
- **RN-002:** serviço e horário de entrada pertencem à participação na fila, ainda que a fonte os agrupe entre os dados indispensáveis. Não devem ser atributos permanentes do paciente.
- **RN-003:** o CPF é o identificador principal e não pode ser duplicado.
- **RN-004:** sem CPF no primeiro contato, a busca de possível duplicidade considera nome, data de nascimento e telefone; a correção depende de confirmação do gestor.
- **RN-005:** o cadastro provisório contém, no mínimo, nome, telefone e serviço solicitado; os demais dados devem ser completados antes de atendimento comum.
- **RN-006:** paciente representado possui dados próprios e um vínculo separado com responsável contendo nome, CPF, telefone e tipo de vínculo.
- **RN-007:** o sistema não armazena diagnóstico, relato terapêutico, motivo detalhado, conteúdo de sessão ou avaliação de risco.

### Formação e ordenação da fila

- **RN-008:** cada psicólogo possui sua própria fila. A primeira versão admite somente um psicólogo, mas o modelo deve aceitar novos profissionais sem reestruturação do domínio.
- **RN-009:** a entrada ocorre somente após presença confirmada, conferência dos dados mínimos e comando explícito da recepção.
- **RN-010:** a ordem normal usa o momento da confirmação de chegada.
- **RN-011:** prioridades legais podem alterar a ordem quando corretamente registradas com motivo geral.
- **RN-012:** urgência clínica não é uma prioridade calculada pelo sistema; o protocolo da clínica retira o paciente da fila comum com motivo operacional genérico.
- **RN-013:** somente o gestor pode mover manualmente uma pessoa; a ação exige justificativa, autor, data e hora.
- **RN-014:** atendimentos simultâneos por serviço são limitados ao número de postos ativos.
- **RN-014A:** ao terminar o atendimento e o paciente sair, a recepção registra a conclusão; esse evento movimenta a fila e atualiza a ordem das pessoas restantes.

### Chamada, ausência e encerramento

- **RN-015:** ao chamar, o status muda para chamado e inicia uma tolerância de 10 minutos.
- **RN-016:** quem não se apresenta dentro da tolerância é marcado como ausente.
- **RN-017:** é permitido um único retorno ao fim da fila, no mesmo turno.
- **RN-018:** a segunda ausência encerra a participação; outra entrada deve ser criada pela recepção.
- **RN-019:** cancelamento ou desistência retiram a pessoa da fila.
- **RN-020:** cancelar ou concluir exige confirmação.
- **RN-021:** excluir registro, reabrir atendimento concluído, mudar ordem ou alterar horário original exige confirmação do gestor e justificativa.

### Acompanhamento e estimativa

- **RN-022:** o link individual revela somente uma participação, nunca nomes ou posições identificáveis de terceiros.
- **RN-023:** a estimativa considera pessoas à frente, duração média, atendimentos em curso, postos ativos, prioridades e pausas.
- **RN-024:** entrada, chamada, início, conclusão, ausência, cancelamento, mudança de prioridade e alteração de capacidade provocam recálculo imediato.
- **RN-025:** a estimativa deve ser uma faixa aproximada; variação de até 15 minutos é aceitável no MVP.
- **RN-026:** o aviso de aproximação aparece quando houver duas pessoas à frente ou cerca de 20 minutos de espera.
- **RN-027:** mensagens públicas são curtas e neutras e não exibem nome completo, CPF, telefone, serviço, responsável ou informação clínica.

### Concorrência, auditoria e contingência

- **RN-028:** duas recepcionistas e o gestor podem operar simultaneamente.
- **RN-029:** o sistema deve impedir uma segunda chamada do mesmo paciente e avisar sobre alteração concorrente do registro.
- **RN-030:** o histórico registra usuário, ação, data, hora, identificador do paciente e estados anterior e novo.
- **RN-031:** mudança de ordem ou prioridade, cancelamento e reabertura também registram justificativa.
- **RN-032:** contingência manual registra número, nome, telefone, serviço e horário de chegada; a reinserção usa o horário original e confere duplicidade por CPF.
- **RN-033:** casos excepcionais são decididos pelo gestor e registrados com justificativa objetiva, sem conteúdo clínico desnecessário.

### Retenção e privacidade

- **RN-034:** registros identificáveis da fila são mantidos por 90 dias após o atendimento e depois excluídos ou anonimizados para relatórios.
- **RN-035:** o gestor pode corrigir dados; pedidos de acesso ou exclusão são recebidos pela administração e analisados conforme as obrigações aplicáveis.
- **RN-036:** backups são diários, protegidos e mantidos por 30 dias.
- **RN-037:** o gestor centraliza solicitações de privacidade até que outro responsável seja formalmente definido.

## Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF-001 | Operar em computadores com Chrome ou Edge e em celulares Android/iPhone por interface responsiva. |
| RNF-002 | Permanecer utilizável em Wi-Fi ou dados móveis instáveis. |
| RNF-003 | Oferecer linguagem simples, contraste adequado, texto legível, teclado e identificação para leitores de tela. |
| RNF-004 | Manter atualizações visíveis aos operadores concorrentes e ao paciente após eventos relevantes. |
| RNF-005 | Impedir exposição de dados, acesso indevido, chamadas duplicadas, perda de registros e cruzamento entre links de pacientes. |
| RNF-006 | Ser de baixo custo e não depender de integrações pagas no MVP. |
| RNF-007 | Ter procedimento manual para indisponibilidade de até 30 minutos e restabelecimento no mesmo turno. |
| RNF-008 | Permitir restauração esperada do serviço em até quatro horas após falha coberta pelo backup. |
| RNF-009 | Tratar dados conforme necessidade, finalidade, segurança e regras de privacidade da clínica. |

## Falhas que bloqueiam o aceite

- exposição de dados pessoais;
- ordem incorreta ou prioridade legal desrespeitada;
- chamadas duplicadas;
- perda de registros;
- acesso indevido;
- link exibindo dados de outra pessoa;
- estimativa sem recálculo após mudança relevante.
