# ReservaLab

API acadêmica para reservar salas de estudo, impedir conflitos de horário e cancelar reservas. A Entrega 1 foi estruturada com especificação técnica, desenvolvimento orientado pela especificação (SDD), ambiente reproduzível e harness de testes automatizados.

**Repositório público:** <https://github.com/herethere04/reservalab-sdd>

## Equipe e contribuições registradas

| Integrante | RA | Atividade registrada |
| --- | --- | --- |
| Áquila de Brito Barbosa | 22453948 | Governança, implementação inicial, configuração do fluxo de IA, revisão final e PDF. |
| Gabriel Ferreira Costa | 22450586 | Validação da especificação e dos contratos, com exemplos práticos; reprodução local do ambiente Docker. |
| Pedro Ivo Gonçalves Pinheiro Coelho | 22453629 | Validação das regras e persistência, abertura do PR de integração #11 e conferência do pipeline. |
| Eduardo Cabral Nunes | 22454089 | Refinamento de concorrência; conferência remota do harness e do artefato do GitHub Actions. |

O escopo e a divisão da sprint estão nas [Issues](https://github.com/herethere04/reservalab-sdd/issues), em [SPRINT.md](docs/SPRINT.md) e em [TEAM.md](docs/TEAM.md). O histórico de revisão e aprovação está nos Pull Requests [#9](https://github.com/herethere04/reservalab-sdd/pull/9), [#10](https://github.com/herethere04/reservalab-sdd/pull/10), [#11](https://github.com/herethere04/reservalab-sdd/pull/11) e [#12](https://github.com/herethere04/reservalab-sdd/pull/12).

## Instalação e execução

Requisitos: Git e Python 3.12 ou superior. O projeto usa somente a biblioteca padrão do Python e SQLite.

```sh
git clone https://github.com/herethere04/reservalab-sdd.git
cd reservalab-sdd
python scripts/run_tests.py --output-dir evidence/latest
python -m reservalab --host 127.0.0.1 --port 8000 --db data/reservalab.db
```

A API responde em `http://127.0.0.1:8000`. Os endpoints principais são `GET /health`, `GET /rooms`, `GET /bookings`, `POST /bookings` e `DELETE /bookings/{id}`.

## Ambiente padronizado

O `Dockerfile` fixa Python 3.13.7 e `compose.yaml` fornece serviços separados para a API e para os testes.

```sh
docker compose run --build --rm tests
docker compose up --build -d api
docker compose logs api
docker compose down
```

O primeiro comando executa o harness e grava `evidence/latest/tests.log` e `evidence/latest/summary.json`.

## Especificação SDD

- [SPEC.md](docs/SPEC.md): problema, requisitos funcionais e não funcionais, regras de negócio, contratos de entrada e saída e critérios de aceite.
- [ARCHITECTURE.md](docs/ARCHITECTURE.md): componentes isolados, APIs e decisões arquiteturais.
- [REFINEMENTS.md](docs/REFINEMENTS.md): ajustes motivados por testes, revisões e validações práticas.
- [AI_WORKFLOW.md](docs/AI_WORKFLOW.md) e [AGENTS.md](AGENTS.md): ferramenta de IA, contexto, regras e ciclo requisito → teste → código → evidência.

## Arquitetura e decisões

Fluxo principal: `HTTP → serviço → validação/repositório SQLite`. O domínio não depende do adaptador HTTP, e a verificação de conflitos e a gravação usam a mesma transação.

| ADR | Decisão | Motivo |
| --- | --- | --- |
| 001 | Python e biblioteca padrão | Ambiente simples e sem dependências externas. |
| 002 | SQLite com `BEGIN IMMEDIATE` | Persistência local e proteção contra dupla reserva concorrente. |
| 003 | UTC e intervalos `[início,fim)` | Comparações previsíveis e reservas adjacentes permitidas. |
| 004 | Cancelamento lógico idempotente | Preservar o histórico e aceitar repetição segura. |
| 005 | Relógio injetável e banco temporário | Testes determinísticos e isolados. |
| 006 | PR revisado e evidência real | Rastreabilidade das decisões e colaboração da equipe. |

## Test harness e evidências

```sh
python scripts/run_tests.py --output-dir evidence/latest
```

O harness usa `unittest`, bancos temporários, relógio fixo e servidor HTTP real em porta dinâmica. A suíte tem **46 testes** para fluxo principal e casos de borda: capacidade, duração, datas, fusos, adjacência, concorrência, persistência, cancelamento, JSON inválido, mídia inadequada e limite de corpo.

Resultado verificado: **46 testes executados, 0 falhas, 0 erros e `success: true`**. O [Test Harness #19](https://github.com/herethere04/reservalab-sdd/actions/runs/34722723488) também concluiu com sucesso no GitHub Actions. Os detalhes estão em [EXECUTION.md](docs/EXECUTION.md) e em [EVIDENCIA_REMOTA_E1-07.md](docs/EVIDENCIA_REMOTA_E1-07.md).

## Governança

O repositório usa `main`, `develop` e branches `feature/*`. `main` e `develop` são protegidas e exigem Pull Request, aprovação de outro integrante, check `harness` aprovado e conversas resolvidas. As contribuições da entrega foram registradas em Issues e PRs, sem commits de implementação feitos diretamente na branch principal.

## Atendimento à Entrega 1

| Requisito | Evidência | Situação |
| --- | --- | --- |
| Repositório, branches e proteção da principal | Histórico Git, regras de branch e PRs | Atendido |
| Divisão de tarefas | Issues, `SPRINT.md` e `TEAM.md` | Atendido |
| Revisões, comentários e aprovações | PRs #9, #10, #11 e #12 | Atendido |
| README técnico e ADRs | Este arquivo e `ARCHITECTURE.md` | Atendido |
| Especificação, regras e contratos | `SPEC.md` | Atendido |
| Componentes e APIs testáveis | `ARCHITECTURE.md` e seção 7 de `SPEC.md` | Atendido |
| Refinamentos por feedback e testes | `REFINEMENTS.md` | Atendido |
| Configuração e uso de IA | `AGENTS.md` e `AI_WORKFLOW.md` | Atendido |
| Ambiente reproduzível | `Dockerfile`, `compose.yaml` e scripts | Atendido |
| Harness, casos principais e de borda | 46 testes automatizados | Atendido |
| Logs e pipeline | `EXECUTION.md`, evidências e GitHub Actions | Atendido |

Cada integrante deve submeter no Moodle o mesmo PDF final com o link do repositório, nomes e RAs, resumo do ambiente e da IA, comandos do harness e a evidência do pipeline.
