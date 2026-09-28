# Decisões e pendências

## Decisões confirmadas

- **DEC-001:** o projeto atual atende uma clínica de psicologia específica, não um SaaS white label.
- **DEC-002:** o MVP possui dois perfis internos: recepção e gestor.
- **DEC-003:** cada profissional usa conta própria; contas compartilhadas são proibidas.
- **DEC-004:** pacientes não têm conta no MVP; usam link individual de uma entrada.
- **DEC-005:** psicólogos não têm acesso direto no MVP.
- **DEC-006:** a sessão interna encerra após 15 minutos sem uso e possui logout manual.
- **DEC-007:** a recuperação de acesso é confirmada pelo gestor.
- **DEC-008:** autenticação em dois fatores fica após o MVP.
- **DEC-009:** dados clínicos e prontuário não fazem parte do sistema.
- **DEC-010:** ações críticas e alterações de estado precisam ser rastreáveis ao usuário.
- **DEC-011:** o gestor valida requisitos e mudanças; o coordenador administrativo o substitui.
- **DEC-012:** o login interno utiliza nome de usuário.
- **DEC-013:** somente o gestor cria, ativa, desativa e altera perfis de contas internas.
- **DEC-014:** a equipe técnica recupera a conta do próprio gestor de forma assistida por comando seguro da aplicação.
- **DEC-015:** senhas possuem oito ou mais caracteres, maiúscula, minúscula, número e caractere especial.
- **DEC-016:** cinco falhas consecutivas geram bloqueio temporário; o prazo inicial adotado é de 15 minutos.
- **DEC-017:** uma conta mantém somente uma sessão ativa por vez.
- **DEC-018:** a recepção poderá consultar histórico ou relatório limitado, com capacidades refinadas quando esses módulos forem implementados.
- **DEC-019:** o link do paciente expira quando o atendimento é concluído e o cancelamento não exige confirmação de identidade adicional.
- **DEC-020:** a primeira versão considera um único psicólogo, mas cada psicólogo terá uma fila própria e o modelo aceitará novos profissionais futuramente.

## Pendências de autenticação e autorização

| ID | Pergunta a validar | Impacto |
|---|---|---|
| PEN-AUT-003 | Como será entregue a primeira credencial e será obrigatória a troca no primeiro acesso? | Segurança da ativação. |
| PEN-AUT-006 | O que exatamente conta como “uso” para renovar os 15 minutos de inatividade? | Consistência entre frontend e backend. |
| PEN-AUT-007 | Deve existir aviso antes da expiração e possibilidade de continuar a sessão? | UX e acessibilidade. |
| PEN-AUT-010 | A troca ou recuperação de senha invalida todas as sessões existentes? | Resposta a comprometimento. |
| PEN-AUT-011 | Quais eventos de autenticação devem ir para auditoria e por quanto tempo? | Segurança, privacidade e `PB16`. |
| PEN-AUT-015 | Como proceder se o paciente compartilhar ou perder o link? | Revogação e reemissão. |

## Pendências gerais do negócio

| ID | Pergunta a validar | Impacto |
|---|---|---|
| PEN-001 | Quais são os nomes finais dos serviços e os tempos médios após o piloto? | Configuração e estimativa. |
| PEN-002 | Quem será formalmente responsável por privacidade e qual orientação jurídica será adotada? | LGPD, solicitações e contratos. |
| PEN-003 | Qual é a data planejada de implantação? | Cronograma e piloto. |
| PEN-004 | A retenção de 90 dias aplica-se só às entradas na fila ou também ao cadastro do paciente? | Modelo de dados e exclusão. |
| PEN-005 | Por quanto tempo permanecem eventos de auditoria, relatórios anonimizados e contas desativadas? | Retenção e compliance. |
| PEN-006 | Como a exclusão aos 90 dias se propaga para backups mantidos por 30 dias? | Política de backup e restauração. |
| PEN-007 | O cadastro completo deve obrigatoriamente existir antes de incluir na fila na Sprint 1, já que o provisório está na Sprint 5? | Fluxo inicial e critérios de `PB03`. |
| PEN-008 | Quais categorias exatas de prioridade legal serão configuradas e como desempatar entradas prioritárias? | Ordenação correta. |
| PEN-009 | Como ordenar prioridade legal em relação à hora de chegada e entre categorias distintas? | Algoritmo de fila e aceite. |
| PEN-010 | Como tratar transferência para o turno seguinte: manter horário, criar nova entrada ou exigir nova confirmação? | Fechamento e auditoria. |
| PEN-011 | Qual é a máquina de estados oficial e quais transições podem ser revertidas? | Domínio, telas e testes. |
| PEN-012 | “Vez próxima” é estado persistido ou condição calculada? | Atualização e auditoria. |
| PEN-013 | Como registrar a restrição a profissional específico sem expor informação sensível? | Capacidade e privacidade. |
| PEN-014 | O gestor também atua como recepção ou apenas administra/configura? | Matriz de autorização. |
| PEN-015 | Quais campos e ações ficam disponíveis quando a conexão está instável, mas não totalmente indisponível? | Experiência e consistência. |
| PEN-016 | Além do nome e do estado ativo, quais dados cadastrais do psicólogo serão exigidos (por exemplo, CRP) e quem poderá consultá-los? | Modelo, validações, permissões e privacidade do cadastro profissional. |

## Hipóteses de trabalho que não são decisões

- **HIP-001:** o backend será a fonte definitiva de autorização; a interface apenas refletirá as permissões.
- **HIP-002:** pacientes, entradas na fila e usuários internos serão conceitos separados.
- **HIP-003:** tokens de paciente e sessões internas terão mecanismos separados.
- **HIP-004:** eventos de auditoria serão imutáveis para usuários comuns.
- **HIP-005:** erros de autenticação não informarão se o identificador existe.

Essas hipóteses seguem boas práticas e os objetivos do projeto, mas devem ser promovidas a decisão técnica somente quando a arquitetura for discutida.

## Processo de decisão

Ao resolver uma pendência:

1. registrar a resposta, responsável, data e canal de validação;
2. criar ou atualizar uma `DEC-xxx`;
3. alterar requisitos, regras, critérios e modelo conceitual afetados;
4. remover a pendência somente depois de verificar que não há documentos contraditórios.
