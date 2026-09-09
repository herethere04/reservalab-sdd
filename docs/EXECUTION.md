# Relatório de execução

## Execução local após revisão técnica

Em 2026-09-09, o harness executou 46 testes com sucesso em Windows e CPython 3.12.14. Logs preservados em [evidence/post-review-local](../evidence/post-review-local). O resumo inclui hashes dos arquivos medidos. Essa execução antecede o primeiro commit de implementação; não é apresentada como execução Docker.

## Execução padronizada no GitHub Actions

O [pipeline do PR #9](https://github.com/herethere04/reservalab-sdd/actions/runs/34387463673) foi executado em 2026-09-09 e concluído com sucesso. O job `harness` construiu a imagem do Dockerfile com CPython 3.13.7 e executou os **46 testes** dentro do contêiner Linux: 0 falhas, 0 erros e 0 ignorados, em 7,831 segundos. As etapas de checkout, build, harness e publicação de logs foram aprovadas.

O artefato `harness-34387463673` contém `tests.log` e `summary.json`, tem digest SHA-256 `13f7f7a98881bff23b17bd2c19b3ab3497eed27cd2441473d023f66f093c6f67` e fica disponível no GitHub por 30 dias. O manifesto dos 12 arquivos executados foi `d2a79fd1159db24ee9d92acc9911e0b503d4c78d1ae2ad9847ebe20014206862`.

O log também revelou uma mensagem tardia e inofensiva ao finalizar o espelho de saída depois do fechamento do arquivo. O harness foi ajustado para tolerar essa ordem de finalização; a nova execução do PR deve confirmar a ausência da mensagem.

## Governança

As proteções de main e develop foram consultadas pela API em 2026-09-09: uma aprovação obrigatória, check harness obrigatório e restrições aplicadas ao administrador. Revisões humanas e merges permanecem pendentes.
