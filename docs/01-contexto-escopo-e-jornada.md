# Contexto, escopo e jornada

## Visão do produto

O sistema organizará filas de atendimento de uma única clínica de psicologia e permitirá que o paciente acompanhe a própria espera de forma segura. O valor central é reduzir a incerteza do paciente, o trabalho repetitivo da recepção e as desistências causadas pela falta de informação.

O produto atual não será uma plataforma SaaS white label. A arquitetura futura pode evitar acoplamentos desnecessários, mas não deve incluir multitenancy, customização por cliente ou operação multiunidade sem aprovação de novo escopo.

## Problema atual

- A fila é controlada com anotações e conferência verbal.
- A recepção gasta tempo explicando a ordem e a espera.
- Mudanças de ordem e atrasos exigem recálculo manual.
- Várias pessoas atualizando anotações provocam retrabalho e risco de conflito.
- É difícil localizar quem decidiu aguardar fora da clínica.
- Pacientes podem desistir porque precisam permanecer no local sem previsão.

## Resultados esperados

- fila organizada e coerente com a ordem e as prioridades aplicáveis;
- menos perguntas à recepção sobre posição e espera;
- menos desistências por falta de informação;
- liberdade para o paciente aguardar fora da clínica;
- atualização confiável da posição e da estimativa;
- proteção contra exposição ou acesso indevido a dados pessoais.

## Atores do MVP

### Recepção

Localiza ou cadastra pacientes, confirma presença, inclui na fila, chama, registra retorno, inicia e conclui atendimento, registra ausência, cancela e opera a capacidade disponível. Pode consultar dados necessários à operação, mas não acessa configurações exclusivas do gestor.

### Gestor

Possui as capacidades operacionais necessárias e também configura serviços, horários, postos, tolerâncias, mensagens e categorias de prioridade; corrige a ordem com justificativa; acessa histórico e relatórios; confirma ações críticas e decide exceções.

### Paciente

Não possui conta interna no MVP. Recebe um link individual para consultar apenas a própria entrada na fila, com posição, quantidade de pessoas à frente, faixa estimada e status. Pode solicitar o cancelamento por esse acesso.

### Psicólogo

Não acessa diretamente o sistema no MVP. Informa disponibilidade à recepção e orienta o encaminhamento quando houver dúvida clínica. Urgências e decisões clínicas permanecem fora do sistema. A primeira versão operacional considerará um único psicólogo, mas o domínio deve permitir cadastrar outros futuramente. Cada psicólogo terá sua própria fila, operada pela recepção.

## Jornada principal futura

1. O paciente chega e informa os dados e o serviço procurado.
2. A recepção localiza o cadastro ou cria um cadastro permitido pelo escopo da fase.
3. A recepção confirma a presença e os dados mínimos.
4. A recepção escolhe o serviço e inclui o paciente na fila correspondente.
5. O sistema registra o horário de entrada e gera o acesso individual.
6. A recepção envia manualmente o link pelo WhatsApp institucional.
7. O paciente pode sair da clínica e acompanhar posição, pessoas à frente, faixa de espera e status.
8. Quando houver duas pessoas à frente ou aproximadamente 20 minutos, a página destaca que a vez está próxima.
9. A recepção chama o próximo paciente. O paciente tem até 10 minutos para se apresentar.
10. A recepção confirma o retorno e registra o início do atendimento.
11. Ao final, a recepção conclui o atendimento.
12. A fila, as estimativas, o histórico e o relatório são atualizados nos eventos correspondentes.

## Escopo confirmado do MVP

- contas individuais e acesso controlado para recepção e gestor;
- cadastro e localização de paciente;
- configuração de serviços, horários e capacidade;
- fila vinculada ao psicólogo responsável, começando com um único profissional;
- confirmação de chegada e ordenação;
- prioridade legal registrada;
- painel operacional concorrente;
- chamada, início, conclusão, ausência, cancelamento e um retorno permitido;
- correção manual da ordem pelo gestor com justificativa;
- acompanhamento por link individual;
- posição, faixa de espera, status e recálculo;
- avisos neutros na página;
- privacidade, autorização e auditoria;
- relatório básico em tela e CSV;
- backup diário e procedimento de contingência.

## Fora do MVP

- prontuário psicológico e conteúdo de sessões;
- diagnóstico, motivo detalhado ou triagem clínica automática;
- agendamento, pagamento, faturamento e teleatendimento;
- cadastro autônomo pelo paciente;
- integração automática com WhatsApp, SMS ou e-mail;
- integração com agenda ou prontuário;
- autenticação em dois fatores;
- operação em várias unidades;
- relatórios avançados.

## Operação esperada

- Unidade: uma única unidade no MVP.
- Funcionamento: segunda a sexta, 8h–12h e 13h–17h.
- Entrada: deve encerrar uma hora antes do fim do turno, ou antes quando não houver capacidade.
- Volume inicial: até 30 pacientes por dia, pico de 10 aguardando, duas filas ativas e até cinco usuários internos.
- Serviços iniciais: acolhimento inicial, média de 20 minutos; atendimento psicológico, média de 50 minutos. Os nomes finais e tempos devem ser revistos após o piloto.
- Piloto: uma semana, em um serviço e um turno; uma hora de treinamento; folha manual também usada nos dois primeiros dias.
