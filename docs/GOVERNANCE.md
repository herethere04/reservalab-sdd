# Governança - estado da Entrega 3

Consulta de 20/10/2026: main em `5be5482caab6e46f1318e70a6bf8ba5ed62afef8`, que integra o PR #20; nenhum PR aberto na consulta inicial. A proposta da Entrega 3 é rastreada por #21 e ainda exige revisão, homologação e promoção revisada. Não há tag/release oficial v1.0.0 na consulta inicial dos refs.

| PR | Resultado verificado |
| --- | --- |
| #15 | Integrado em develop em 15/10 UTC, após aprovação de Claneeer. |
| #13 | Integrado em main em 16/10 UTC; revisão atualizada APPROVED de g0bss no head d1b38d. A aprovação antiga de eddyocn foi DISMISSED. |
| #19 | Atualização do relatório/PDF aprovada por g0bss e integrada em develop em 16/10 UTC. |
| #20 | Integrado em main em 18/10 UTC; g0bss registrou APPROVED em 18/10 às 02:14 UTC antes do merge. O comentário de Claneeer é COMMENTED e não é contado como aprovação formal. |

Na tentativa assistida anterior, o GitHub recusou o merge sem nova aprovação, demonstrando a exigência aplicada naquele momento. Não se declara auditoria de todas as configurações atuais de proteção; o workflow final também confere a flag protected de main antes da release. Nenhuma regra foi reduzida nesta preparação.

A nova etapa mantém feature/* → develop → main com check harness e revisão de outra pessoa. Os responsáveis registram validação/aceite com suas próprias contas. Preparação, logs e documentos do Codex não são autoria, execução ou aprovação pessoal dos colegas. A release só é declarada publicada depois da ação efetiva no GitHub.

## Registro histórico da consulta da Entrega 2

O texto abaixo é o snapshot de 14/10; estados como PR #13 aberto são históricos e foram superados pelos eventos da tabela acima.

# Governança verificada - Entrega 2

Consulta: 14/10/2026. Fonte: conector GitHub, metadados de Issues/PRs e revisões. Snapshot em [evidence/entrega2-governanca/snapshot.json](../evidence/entrega2-governanca/snapshot.json). A existência de proteção em setembro não comprova sua configuração atual; ela não foi reconsultada nesta etapa.

| PR | Autor da conta | Fluxo real | Revisão válida observada | Estado |
| --- | --- | --- | --- | --- |
| [#9](https://github.com/herethere04/reservalab-sdd/pull/9) | herethere04 | feature/entrega-inicial -> develop | g0bss, APPROVED, 10/09, antes do merge | Integrado 10/09 |
| [#10](https://github.com/herethere04/reservalab-sdd/pull/10) | g0bss | feature/revisao-especificacao -> develop | herethere04, APPROVED, 13/09, antes do merge | Integrado 13/09 |
| [#11](https://github.com/herethere04/reservalab-sdd/pull/11) | Claneeer | feature/validacao-reservas -> main | eddyocn, APPROVED, 12/09, antes do merge | Integrado 12/09 |
| [#12](https://github.com/herethere04/reservalab-sdd/pull/12) | g0bss | feature/harness-evidencias -> develop | herethere04, APPROVED, 13/09, após aprovação anterior descartada | Integrado 13/09 |
| [#13](https://github.com/herethere04/reservalab-sdd/pull/13) | herethere04 | develop -> main | eddyocn, APPROVED, 13/09 | Aberto; não integrado na consulta |

As Issues #1 a #8 estão fechadas no GitHub. Alguns textos mantêm checklists ou frases de preparação pendente. O estado fechado não prova sozinho todos os critérios: deve ser confrontado com PRs, comentários e evidências. A Issue #8 está fechada apesar de #13 continuar aberto, mostrando uma diferença entre rastreamento de tarefa e integração.

O PR #11 possui aprovação de outra conta, mas usou main como base, contrariando o percurso planejado por ADR-006. O relatório registra a exceção e preserva o histórico. Os PRs #11 e #13 não podem ser apresentados como se formassem uma promoção já concluída e rigorosamente conforme o fluxo.

A descrição do PR #12 atribui a reprodução do ambiente a Eduardo, enquanto o autor GitHub é g0bss. O relatório distingue a conta autora do PR da contribuição narrada. O comentário de eddyocn na Issue #7 comprova que essa conta vinculou a evidência remota ao PR #12; não se presume autoria de cada linha.

## Critérios para o novo PR

1. Base develop; branch feature/entrega-2; Issue #14 vinculada.
2. SPEC, refinamentos, testes e documentação coerentes.
3. Job harness aprovado para o commit final; consultar novamente se houver novos commits.
4. Outro integrante deve ler o diff, reproduzir os testes pertinentes e registrar revisão com a própria conta.
5. Pedidos de alteração resolvidos antes do merge; promoção para main por PR com revisão humana.
6. Conferir o estado de #13 antes da promoção para evitar duas integrações concorrentes sobre o mesmo escopo.
7. Atualizar o PDF/links se houver mudanças materiais após esta versão.

A preparação por IA não produz aprovação humana. Não foram alteradas regras de proteção nem realizados merges nesta etapa.

