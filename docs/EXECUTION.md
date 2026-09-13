# Relatório de execução

## Execução local após revisão técnica

Em 2026-09-09, o harness executou 46 testes com sucesso em Windows e CPython 3.12.14. Logs preservados em [evidence/post-review-local](../evidence/post-review-local). O resumo inclui hashes dos arquivos medidos. Essa execução antecede o primeiro commit de implementação; não é apresentada como execução Docker.

## Execução padronizada no GitHub Actions

O [pipeline após a correção do PR #9](https://github.com/herethere04/reservalab-sdd/actions/runs/34387758154) foi executado em 2026-09-09 e concluído com sucesso. O job `harness` construiu a imagem do Dockerfile com CPython 3.13.7 e executou os **46 testes** dentro do contêiner Linux: 0 falhas, 0 erros e 0 ignorados, em 7,330 segundos. As etapas de checkout, build, harness e publicação de logs foram aprovadas.

O artefato `harness-34387758154` contém `tests.log` e `summary.json`, tem digest SHA-256 `dc37bc39e1e06ee6e3c4007490e6384b34b2f10b9a14db9ce75a82a272edca86` e fica disponível no GitHub por 30 dias.

Uma execução anterior revelou uma mensagem tardia e inofensiva ao finalizar o espelho de saída depois do fechamento do arquivo. O harness foi ajustado para tolerar essa ordem; o pipeline final confirmou a correção sem repetir a mensagem.

## Governança

As proteções de main e develop foram consultadas pela API em 2026-09-09: uma aprovação obrigatória, check harness obrigatório e restrições aplicadas ao administrador. Revisões humanas e merges permanecem pendentes.

## Execução local padronizada via Docker (Issue E1-04)

Em 2026-09-12, a execução do *harness* via Docker Compose (`docker compose run --build --rm tests`) foi reproduzida com sucesso no ambiente local. 

**Resumo da evidência real:**
* **Ambiente:** Linux (WSL2) com Python 3.13.7 (CPython)
* **Testes:** 46 executados, 0 falhas, 0 erros (`success: true`)
* **Duração:** 8.314 segundos
* **Manifesto SHA-256 (12 arquivos):** `113e9c49a93b214fe3167f4240bb5dac1a6795ff2b89bc3b639d822729cf2832`

A execução confirmou que a infraestrutura em contêiner atende aos requisitos de isolamento e padronização da entrega.