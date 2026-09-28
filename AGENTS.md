# Instruções persistentes do projeto

Antes de analisar, planejar ou implementar qualquer mudança, leia `docs/README.md` e os documentos que ele classifica como fontes de verdade para o assunto em questão.

## Estado atual

- A implementação autorizada cobre autenticação e gestão de contas internas, além do cadastro de psicólogos e da estrutura mínima de uma fila própria por profissional.
- Não criar modelo, API, tela, formulário ou validação de cadastro de pacientes; esse item pertence a outro integrante.
- A entidade `Fila` existente representa somente o vínculo individual com o psicólogo. Não implementar entradas, ordenação, chamada, atendimento ou o fluxo completo de filas sem solicitação explícita.
- O produto atual é específico para uma clínica de psicologia. Não introduzir multiempresa, multitenancy ou white label sem mudança de escopo validada.

## Regras de trabalho futuras

- Distinguir sempre fato confirmado, requisito derivado, proposta técnica e dúvida pendente.
- Não inventar regra de negócio para preencher lacunas. Registrar a lacuna em `docs/06-decisoes-e-pendencias.md`.
- Manter backend, frontend, banco, testes e documentação coerentes com as mesmas regras.
- Proteger dados pessoais por padrão e não registrar dados clínicos, diagnóstico, motivo detalhado da consulta ou conteúdo terapêutico.
- Preservar a separação conceitual entre cadastro do paciente e participação do paciente em uma fila.
- Atualizar a documentação relevante junto com qualquer decisão ou mudança funcional.
- Aplicar código limpo, princípios de design, testes proporcionais ao risco e práticas idiomáticas de Python, Django e React quando a implementação for autorizada.
- Usar commits pequenos, coesos e revisáveis, seguindo o padrão definido em `docs/07-diretrizes-de-engenharia-e-git.md`.
