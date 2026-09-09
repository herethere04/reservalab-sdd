# Conferência da Entrega 1

Esta lista diferencia artefatos verificáveis de atividades humanas. Marque um item apenas após conferir a evidência correspondente. A preparação automatizada não conclui revisões entre colegas nem submete no Moodle.

| Exigência | Onde conferir | Critério de fechamento |
| --- | --- | --- |
| Repositório público ou acessível ao professor | URL do README/PDF e configurações do GitHub | Professor consegue abrir código, Issues e evidências. |
| Branches e ausência de commits diretos em `main` | Histórico, branches, PRs e regras do GitHub | Fluxo principal protegido/verificado; alterações entram por PR. |
| Divisão de trabalho | Issues e `docs/SPRINT.md` | Responsáveis, escopo, aceite e progresso registrados. |
| Revisões reais antes do merge | Aba Files changed / Reviews dos PRs | Outro integrante revisou o commit relevante, comentou e aprovou. |
| Visão geral, execução e decisões | `README.md` e `docs/ARCHITECTURE.md` | Um colega segue o guia e compreende as escolhas. |
| Especificação SDD | `docs/SPEC.md` | RF, RNF, regras, contratos, decomposição e cenários conferidos. |
| Refinamento por feedback | `docs/REFINEMENTS.md` e PR/Issue ligado | Pelo menos um registro real de teste ou revisão que confirme/ajuste o contrato, com origem clara. |
| Agente de IA configurado e uso documentado | `AGENTS.md` e `docs/AI_WORKFLOW.md` | Contexto, regras, ferramenta e participação relatados com precisão. |
| Ambiente padronizado | Dockerfile, composição/scripts e README | Execução reproduzível comprovada no ambiente efetivamente usado. |
| Harness e casos iniciais | Suíte e comandos no README | Casos principais, limites e concorrência com sucesso. |
| Logs/prints do pipeline | Artefatos, relatório e execução do GitHub Actions | Evidência identifica execução e commit correspondentes. |
| PDF único | Arquivo de entrega | URL, quatro nomes/RAs, resumo de ambiente/IA, comandos e logs/prints legíveis. |
| Submissão de todos | Moodle, por cada integrante | Os quatro integrantes enviaram o mesmo PDF final. |

## Pendências que exigem os integrantes

- Enquanto o PR inicial para `develop` estiver aberto, executar a implementação em `feature/entrega-inicial`. Não supor que a aplicação já está em `develop` ou `main`.
- Cada colega deve usar sua própria conta para assumir a tarefa, executar sua conferência e revisar o PR inicial no seu escopo. Registrar procedimentos e resultados efetivamente observados.
- O autor do PR não pode produzir a aprovação do próprio trabalho nem atribuí-la aos colegas.
- O PR inicial deve receber aprovação real de pelo menos outro integrante, respeitando também a quantidade configurada nas regras do repositório. Não se exigem quatro aprovações fictícias; cada integrante deve evidenciar sua contribuição real.
- Merges devem aguardar os checks e as revisões humanas exigidas. Depois do merge inicial em `develop`, abrir branches de contribuição a partir dela somente para ajustes necessários e refinamentos justificados.
- Uma conferência que não encontre defeitos pode ser documentada em comentário de revisão ou Issue com evidências. Não fabricar falhas nem alterações para aparentar desenvolvimento anterior dos colegas.
- Se houver mudanças depois de gerar o PDF, atualizar os links e evidências da versão final.
- Cada um dos quatro integrantes deve enviar o PDF no Moodle.

## Sequência para concluir a colaboração

1. Identificar os usuários GitHub, habilitar o acesso necessário e vincular os responsáveis às Issues.
2. Gabriel, Pedro e Eduardo executam suas verificações em `feature/entrega-inicial` e registram os achados com suas próprias contas. Áquila responde às revisões e acompanha os checks.
3. Corrigir os pontos encontrados, se houver, e solicitar nova conferência das alterações relevantes. Obter a aprovação humana exigida antes de integrar o PR inicial em `develop`.
4. Realizar contribuições posteriores em branches próprias baseadas em `develop`; revisar os PRs conforme a distribuição de `docs/TEAM.md`.
5. Abrir e revisar o PR de `develop` para `main`, conferir as evidências finais e realizar o merge após os critérios exigidos.
6. Atualizar o PDF final, compartilhá-lo com o grupo e cada integrante submetê-lo no Moodle.

O registro de refinamentos técnicos entre agentes em `docs/REFINEMENTS.md` já identifica correções e testes reais da preparação. Ele auxilia a revisão dos integrantes e não substitui seus comentários ou aprovações.

## Conteúdo mínimo do PDF

1. Título da atividade e projeto ReservaLab.
2. Link direto e clicável do repositório, com acesso verificado.
3. Áquila de Brito Barbosa — 22453948; Gabriel Ferreira Costa — 22450586; Pedro Ivo Gonçalves Pinheiro Coelho — 22453629; Eduardo Cabral Nunes — 22454089.
4. Resumo do problema, Python/SQLite, ambiente padronizado e Codex utilizado.
5. Comandos exatos para executar o harness.
6. Logs ou capturas de execução bem-sucedida, com data, versão e referência ao pipeline/commit quando disponíveis.

O PDF deve distinguir execução local, execução em contêiner e execução no GitHub Actions. Uma configuração escrita não comprova que o respectivo ambiente foi executado.
