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

