# Relatório de execução

## Execução local após revisão técnica

Em 2026-09-09, o harness executou 46 testes com sucesso em Windows e CPython 3.12.14. Logs preservados em [evidence/post-review-local](../evidence/post-review-local). O resumo inclui hashes dos arquivos medidos. Essa execução antecede o primeiro commit de implementação; não é apresentada como execução Docker.

## Execução padronizada no GitHub Actions

O [pipeline após a correção do PR #9](https://github.com/herethere04/reservalab-sdd/actions/runs/34387758154) foi executado em 2026-09-09 e concluído com sucesso. O job `harness` construiu a imagem do Dockerfile com CPython 3.13.7 e executou os **46 testes** dentro do contêiner Linux: 0 falhas, 0 erros e 0 ignorados, em 7,330 segundos. As etapas de checkout, build, harness e publicação de logs foram aprovadas.

O artefato `harness-34387758154` contém `tests.log` e `summary.json`, tem digest SHA-256 `dc37bc39e1e06ee6e3c4007490e6384b34b2f10b9a14db9ce75a82a272edca86` e fica disponível no GitHub por 30 dias.

Uma execução anterior revelou uma mensagem tardia e inofensiva ao finalizar o espelho de saída depois do fechamento do arquivo. O harness foi ajustado para tolerar essa ordem; o pipeline final confirmou a correção sem repetir a mensagem.

## Governança

As proteções de main e develop foram consultadas pela API em 2026-09-09: uma aprovação obrigatória, check harness obrigatório e restrições aplicadas ao administrador. Este era o estado em 09/09/2026. A consulta de 14/10/2026 confirma merges e aprovações dos PRs #9, #10, #11 e #12; o PR #13 continua aberto. Ver `GOVERNANCE.md` para a auditoria atual, incluindo a exceção de fluxo do PR #11. As proteções atuais não foram reconsultadas nesta etapa.

## Execução local padronizada via Docker (Issue E1-04)

Em 2026-09-12, a execução do *harness* via Docker Compose (`docker compose run --build --rm tests`) foi reproduzida com sucesso no ambiente local. 

**Resumo da evidência real:**
* **Ambiente:** Linux (WSL2) com Python 3.13.7 (CPython)
* **Testes:** 46 executados, 0 falhas, 0 erros (`success: true`)
* **Duração:** 8.314 segundos
* **Manifesto SHA-256 (12 arquivos):** `113e9c49a93b214fe3167f4240bb5dac1a6795ff2b89bc3b639d822729cf2832`

A execução confirmou que a infraestrutura em contêiner atende aos requisitos de isolamento e padronização da entrega.

## Entrega 2 - execução real em 14/10/2026

A cópia isolada foi obtida de `develop` no commit `bffa8f1c0ce0a5ecf11007598cf0e133d40e7dd6`.

| Execução | Resultado | Evidência |
| --- | --- | --- |
| Inicial, com sockets bloqueados pelo ambiente | 46 testes, 14 erros HTTP, saída 1 | `evidence/entrega2-baseline/` |
| Mesmos fontes, sockets locais permitidos | 46 testes, 0 falhas, 0 erros, saída 0 | `evidence/entrega2-local-baseline/` |
| Suíte ampliada, CPython 3.12.3 / Linux | 50 testes, 0 falhas, 0 erros, 0 ignorados, saída 0 | `evidence/entrega2-local/` |

Comando final: `python3 scripts/run_tests.py --output-dir evidence/entrega2-local`. UTC: `2026-10-14T20:40:09.043554Z`. Duração: 7,750 s. Manifesto dos 16 arquivos medidos: `b4850b422970dac2e71099d34fdcadd26affdd9a76cd3460b062aaa567680f5e`. O Git HEAD do log identifica a base; `working_tree_dirty: true` registra corretamente as alterações ainda não commitadas. O manifesto identifica os fontes efetivamente testados.

A primeira tentativa do Compose não encontrou o daemon acessível. Depois que Áquila abriu o Docker Desktop, a imagem foi construída com sucesso; a execução Compose foi impedida pelo compartilhamento da pasta `/tmp` (mounts denied). A mesma imagem foi executada sem bind mount, com logs salvos dentro do contêiner e recuperados por `docker cp`. O CI do novo PR também deve ser conferido antes do merge.

O conector GitHub confirmou que a execução histórica [34731777935](https://github.com/herethere04/reservalab-sdd/actions/runs/34731777935), associada ao commit `edcef483cf9667fe119b7e1c75e4a95958006be5` do PR #12, terminou com `success`, inclusive build, harness e publicação de logs. Essa confirmação é de estado/etapas e não uma nova reprodução de contagem. Os artefatos históricos têm retenção de 30 dias; a data da Entrega 2 ultrapassa esse prazo, por isso novas evidências versionadas são preservadas.


### Execução Docker atual aprovada

Comandos efetivamente executados após o build da imagem pelo Compose:

```sh
docker run --name reservalab-e2-validation-20261014 reservalab-entrega2-tests python scripts/run_tests.py --output-dir /app/evidence/entrega2-docker
docker cp reservalab-e2-validation-20261014:/app/evidence/entrega2-docker/. evidence/entrega2-docker/
docker rm reservalab-e2-validation-20261014
```

Resultado: CPython 3.13.7, Linux linuxkit/glibc 2.36, 50 testes, zero falhas/erros/ignorados, saída 0, 9,136 segundos. UTC: `2026-10-14T20:48:08.250267Z`. Evidência: [log](../evidence/entrega2-docker/tests.log) e [resumo](../evidence/entrega2-docker/summary.json). Manifesto: `39cf06a52c9bacfb260c774681ecb52725bc2fb0364a59c95f57f8dbdb8ab45e`.

O contêiner não copia `.git`, Dockerfile, Compose ou o workflow; o resumo identifica 13 arquivos e HEAD indisponível. Os hashes dos 13 fontes comuns foram comparados com o resumo local e são iguais. Assim, a diferença entre manifestos corresponde ao conjunto de arquivos medidos, não a uma divergência da aplicação/testes. A execução sem bind mount evita alterar o compartilhamento global de pastas do Docker Desktop.
