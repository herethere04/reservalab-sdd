# Entrega 3 - Documento de encerramento

Issue #21. Prazo do enunciado: **25/10/2026, 23h55 (Brasília)**. Preparação assistida pelo Codex a pedido do usuário; vídeo ainda não gravado/publicado na consulta inicial de 20/10.

## Resultado técnico preparado

Solução funcional da Entrega 1 preservada: API HTTP local de reservas, SQLite transacional, UTC, intervalos semiabertos e cancelamento idempotente. As-Built em [AS_BUILT.md](AS_BUILT.md), contratos em [SPEC.md](SPEC.md), decisões em [ARCHITECTURE.md](ARCHITECTURE.md). Esta etapa adiciona cobertura de linhas e cenários relevantes de protocolo/CLI, roteiro executável de demonstração e fluxo de publicação oficial.

Resultados reais: [execução](EXECUTION.md), [cobertura local](../evidence/entrega3-local/coverage.md), [JSON](../evidence/entrega3-local/coverage.json), [log](../evidence/entrega3-local/tests/tests.log). Percentuais não são preenchidos antes da execução e não se apresentam como cobertura de branches.

## Cinco itens do PDF

| Item | Preparação e fechamento |
| --- | --- |
| Link direto da release v1.0.0 | Publicado pelo workflow manual após homologação/main; endereço previsto não é tratado como release existente. |
| Integrantes e RAs | Dados reais autorizados no README e no gerador/PDF; não são fixtures de testes. |
| Testes e cobertura | Harness real, log/summary, linhas executadas/executáveis e hashes; anexos gerados na publicação. |
| Vídeo funcional 3-5 min | Eduardo grava e publica pela Issue #24; roteiro em DEMO.md. |
| Resumo executivo e lições | PDF gerado com escopo, resultado, limites, retrospectiva e uso de IA sem métricas inventadas. |

A prévia `output/pdf/ReservaLab_Entrega_3_PREPARACAO.pdf` mostra a estrutura e evidências atuais, mas está marcada para não submeter. O PDF definitivo **ReservaLab_Entrega_3.pdf** será anexo da release v1.0.0 e receberá o link real do vídeo informado pela equipe. Guia de geração/publicação: [RELEASE.md](RELEASE.md).

## Retrospectiva fundamentada

O histórico registra refinamentos em fusos, minutos inteiros, Unicode/JSON, identificador SQLite fora de faixa e transação concorrente. Nas entregas intermediárias, o harness passou a testar a própria falha/erro/suíte vazia; a inspeção dos PRs mostrou que checklists e textos podem ficar desatualizados depois de um merge. A etapa final mede cobertura e reforça protocolo/entrada CLI, sem alterar regras de reserva para fabricar uma nova correção.

Somente o Codex teve uso informado pela equipe. Seu apoio se materializou em especificações, código/testes, análise de casos de borda e organização documental. Não houve baseline sem IA nem medição de tempo/custo que permita afirmar ganho percentual de produtividade. O benefício verificável é a existência desses artefatos e das regressões; o grupo deve revisar e compreender o resultado para defendê-lo.

Riscos e limites: alucinação, comandos destrutivos, exposição indevida de contexto e origem/licenciamento de trechos. Foram adotados escopo local, dados fictícios, fontes/execuções reais, hashes e revisões humanas. Os testes não certificam produção; ausência de autenticação/autorização e limites do http.server continuam explicitados. A retrospectiva não inventa entrevistas, participação pessoal ou fala de colegas.

## Pendências humanas

Ver #22, #23 e #24: conferência da especificação, homologação e reprodução, gravação/publicação do vídeo, integração revisada em main, release oficial e conferência do PDF definitivo. A existência do material de preparação não comprova essas ações. Nenhuma submissão acadêmica é presumida.
