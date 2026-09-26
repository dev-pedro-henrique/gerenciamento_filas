# Base de conhecimento do projeto

Esta pasta consolida o entendimento obtido nas fontes de requisitos e deve ser mantida como documentação viva. Ela existe para evitar que regras sejam redescobertas, contraditas ou implementadas de formas diferentes no frontend e no backend.

## Ordem recomendada de leitura

1. [`00-fontes-e-rastreabilidade.md`](00-fontes-e-rastreabilidade.md) — fontes, autoridade e convenções.
2. [`01-contexto-escopo-e-jornada.md`](01-contexto-escopo-e-jornada.md) — problema, objetivos, atores, escopo e fluxo de ponta a ponta.
3. [`02-requisitos-e-regras-de-negocio.md`](02-requisitos-e-regras-de-negocio.md) — catálogo funcional, não funcional e regras operacionais.
4. [`03-autenticacao-autorizacao-e-acessos.md`](03-autenticacao-autorizacao-e-acessos.md) — especificação aprofundada da área sob responsabilidade atual.
5. [`04-modelo-conceitual-do-dominio.md`](04-modelo-conceitual-do-dominio.md) — entidades e relacionamentos conceituais, sem compromisso com implementação.
6. [`05-backlog-cronograma-e-sprint-1.md`](05-backlog-cronograma-e-sprint-1.md) — prioridades e planejamento fornecidos.
7. [`06-decisoes-e-pendencias.md`](06-decisoes-e-pendencias.md) — decisões confirmadas, hipóteses e dúvidas que exigem validação.
8. [`07-diretrizes-de-engenharia-e-git.md`](07-diretrizes-de-engenharia-e-git.md) — padrões a aplicar quando o desenvolvimento começar.
9. [`08-historico-do-projeto.md`](08-historico-do-projeto.md) — evolução documental e marcos do projeto.

## Hierarquia das informações

Quando houver conflito, usar a seguinte ordem até que o gestor valide outra decisão:

1. decisão nova formalmente validada pelo gestor ou, em sua ausência, pelo coordenador administrativo;
2. questionário preenchido e consolidado em 14 de setembro de 2026;
3. documento de perguntas e respostas;
4. product backlog e planejamento da Sprint 1;
5. requisitos derivados registrados nesta pasta;
6. propostas técnicas ainda não aprovadas.

Toda divergência deve ser registrada em `06-decisoes-e-pendencias.md`, sem ser silenciosamente resolvida pela equipe técnica.

## Vocabulário documental

- **Confirmado:** declarado diretamente nas fontes.
- **Derivado:** necessário para satisfazer uma ou mais regras confirmadas, mas não declarado com o mesmo nível de detalhe.
- **Proposto:** recomendação de produto ou engenharia ainda sujeita a aprovação.
- **Pendente:** informação que muda o comportamento esperado e precisa de resposta do responsável pelo negócio.
- **Fora do MVP:** reconhecido, porém adiado ou excluído da primeira versão.
