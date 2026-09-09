# Relatório de execução

## Execução local após revisão técnica

Em 2026-09-09, o harness executou 46 testes com sucesso em Windows e CPython 3.12.14. Logs preservados em [evidence/post-review-local](../evidence/post-review-local). O resumo inclui hashes dos arquivos medidos. Essa execução antecede o primeiro commit de implementação; não é apresentada como execução Docker.

## Execução padronizada

O pipeline `.github/workflows/tests.yml` constrói a imagem definida no Dockerfile e executa o harness no contêiner. A execução remota será vinculada neste documento após verificação do resultado real.

## Governança

As proteções de main e develop foram consultadas pela API em 2026-09-09: uma aprovação obrigatória, check harness obrigatório e restrições aplicadas ao administrador. Revisões humanas e merges permanecem pendentes.
