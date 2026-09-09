# ReservaLab

API simples para reservar salas de estudo, impedir conflitos de horário e cancelar reservas. Projeto acadêmico da **Entrega 1: Ambiente, Especificação Técnica e Test Harness**, desenvolvido com fluxo SDD e auxílio do Codex.

**Estado da entrega:** implementação disponível em [`feature/entrega-inicial`](https://github.com/herethere04/reservalab-sdd/tree/feature/entrega-inicial), aguardando revisão humana antes da integração. `main` e `develop` estão protegidas. A existência de código e testes aprovados não substitui a colaboração dos integrantes.

## Equipe

| Integrante | RA | Responsabilidade |
| --- | --- | --- |
| Áquila de Brito Barbosa | 22453948 | Integração, governança e entrega |
| Gabriel Ferreira Costa | 22450586 | Especificação e contratos |
| Pedro Ivo Gonçalves Pinheiro Coelho | 22453629 | Regras e persistência |
| Eduardo Cabral Nunes | 22454089 | Harness, ambiente e evidências |

As tarefas propostas e os procedimentos individuais estão em [TEAM.md](docs/TEAM.md), [SPRINT.md](docs/SPRINT.md) e nas [Issues](https://github.com/herethere04/reservalab-sdd/issues). As contribuições e aprovações humanas ainda devem ser registradas por cada pessoa em sua conta.

## Instalação e execução local

Requisitos: Git e Python **3.12 ou superior**. Nenhum pacote Python externo, chave de API ou serviço pago é necessário para executar a aplicação e os testes.

```sh
git clone https://github.com/herethere04/reservalab-sdd.git
cd reservalab-sdd
git switch feature/entrega-inicial
python --version
python scripts/run_tests.py --output-dir evidence/latest
python -m reservalab --host 127.0.0.1 --port 8000 --db data/reservalab.db
```

Após a integração do PR, use `git switch develop` para trabalhar sobre a versão integrada. Em sistemas onde o executável se chama `python3`, substitua `python` nos comandos. No Windows, `py -3` também pode ser usado. Encerre a API com `Ctrl+C`.

Abra <http://127.0.0.1:8000/health> ou <http://127.0.0.1:8000/rooms> no navegador para consultar JSON. Não há interface gráfica nesta entrega. O banco local é criado automaticamente e as reservas persistem entre execuções.

## Ambiente padronizado com Docker

Instale e inicie Docker Desktop/Engine com suporte a contêineres Linux e Docker Compose v2. A imagem usa Python **3.13.7**, sem instalação de bibliotecas adicionais.

```sh
docker compose run --build --rm tests
docker compose up --build -d api
docker compose ps
docker compose logs api
docker compose down
```

O primeiro comando salva `evidence/latest/tests.log` e `summary.json`. O serviço fica em `127.0.0.1:8000`, com banco em volume persistente. `docker compose down` preserva o volume. O download inicial da imagem exige acesso à internet; o harness usa apenas recursos locais.

## Test harness

```sh
python scripts/run_tests.py --output-dir evidence/latest
```

O harness executa `unittest` com bancos temporários, relógio fixo e servidor HTTP real em porta dinâmica. Produz log detalhado e resumo JSON com versão, plataforma, contagem, duração, estado do Git e manifesto SHA-256 dos arquivos medidos. Falha de teste ou suíte vazia resulta em código de saída 1; sucesso retorna 0.

A suíte contém **46 testes** cobrindo fluxo completo, limites de duração e capacidade, passado, fusos equivalentes, intervalos adjacentes, conflitos simultâneos, cancelamento idempotente, persistência, JSON e entradas inválidas. Não se declara percentual de cobertura de código.

O [pipeline](.github/workflows/tests.yml) constrói a imagem e executa o mesmo harness dentro do contêiner em pushes de trabalho e PRs para `develop`/`main`. O job obrigatório se chama `harness`; os logs são publicados como artefato do GitHub Actions, inclusive em caso de falha.

### Evidência local verificada

[Log completo](evidence/post-review-local/tests.log) · [Resumo com hashes](evidence/post-review-local/summary.json)

```text
UTC: 2026-09-09T16:35:58.737410Z
Python: 3.12.14 (CPython)
Platform: Windows-11-10.0.26200-SP0
tests_run: 46
failures: 0
errors: 0
skipped: 0
success: true
```

Esta evidência corresponde à execução local após revisão técnica e antes do primeiro commit de implementação. Seu manifesto identifica os arquivos testados. O status e o link da execução no contêiner serão registrados em [EXECUTION.md](docs/EXECUTION.md).

## Contrato resumido

| Método e rota | Resultado |
| --- | --- |
| `GET /health` | 200, `{"status":"ok"}` |
| `GET /rooms` | 200, catálogo de salas |
| `GET /bookings` | 200, reservas ativas e canceladas |
| `POST /bookings` | 201, reserva criada; 409 se houver conflito |
| `DELETE /bookings/{id}` | 200, reserva cancelada; 404 se inexistente |

Exemplo de corpo para `POST /bookings`, enviado com `Content-Type: application/json` (use uma data futura na execução):

```json
{"room_id":1,"student_name":"Estudante Exemplo","starts_at":"2030-10-10T14:00:00-03:00","ends_at":"2030-10-10T15:00:00-03:00","participants":3}
```

PowerShell:

```powershell
$inicio = [DateTimeOffset]::UtcNow.AddDays(1)
$inicio = $inicio.AddTicks(-($inicio.Ticks % [TimeSpan]::TicksPerMinute))
$dados = @{room_id=1; student_name='Estudante Exemplo'; starts_at=$inicio.ToString('o'); ends_at=$inicio.AddHours(1).ToString('o'); participants=3} | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/bookings -Method Post -ContentType 'application/json' -Body $dados
```

Regras: 30 a 120 minutos, fuso explícito, minutos inteiros, início não passado e capacidade respeitada. Reservas consecutivas são permitidas; apenas sobreposição de reservas ativas da mesma sala é bloqueada. Leia a [especificação completa](docs/SPEC.md) para erros, limites e critérios de aceite.

## Arquitetura e ADRs

`HTTP → serviço → validação / repositório SQLite`. O domínio não depende do adaptador HTTP. A consulta de conflitos e a gravação usam a mesma transação para impedir dupla reserva.

| ADR | Decisão | Motivo |
| --- | --- | --- |
| 001 | Python e biblioteca padrão | Baixa complexidade e nenhum pacote extra |
| 002 | SQLite e `BEGIN IMMEDIATE` | Persistência simples e consistência concorrente |
| 003 | UTC e intervalos `[início,fim)` | Comparação previsível e adjacência permitida |
| 004 | Cancelamento lógico idempotente | Preservar histórico e tolerar repetição |
| 005 | Relógio injetável e banco temporário | Testes determinísticos e isolados |
| 006 | PR revisado e evidência autêntica | Rastreabilidade e colaboração verificável |

Contexto, consequências e diagrama em [ARCHITECTURE.md](docs/ARCHITECTURE.md). Refinamentos motivados pela revisão e pelos testes estão em [REFINEMENTS.md](docs/REFINEMENTS.md).

## Governança e IA

O histórico foi inicializado em uma branch de trabalho, renomeada para `bootstrap`; `main` e `develop` foram criadas apontando para essa raiz. A implementação é proposta em `feature/entrega-inicial`. Não foram feitos commits de implementação diretamente em `main` ou `develop`.

As duas branches exigem PR com **uma aprovação de outra pessoa**, check `harness` aprovado e conversas resolvidas; as regras incluem administradores. Novos commits invalidam aprovações antigas. A revisão do último push deve ser feita por outra pessoa. Nenhum merge deve ocorrer antes disso.

O Codex desktop auxiliou na especificação, geração de código, testes e revisão técnica com agentes de escopo separado. [AGENTS.md](AGENTS.md) contém instruções SDD; [AI_WORKFLOW.md](docs/AI_WORKFLOW.md) documenta uso, prompts e limites. Os colegas devem revisar e assumir suas contribuições; não há aprovações simuladas.

## Limites e submissão

Demonstração acadêmica local: sem autenticação, autorização por usuário, frontend ou integração institucional. Qualquer cliente local pode consultar/cancelar reservas; use nomes fictícios. Não há implantação pública do serviço.

Antes de submeter, concluir a [checklist](docs/DELIVERY_CHECKLIST.md), as revisões humanas e os merges. Cada integrante envia no Moodle o mesmo PDF com repositório, nomes/RAs, ambiente, agentes, comandos e evidências.

Referências técnicas: [Python/SQLite](https://docs.python.org/3.13/library/sqlite3.html), [instruções do Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [proteção de branches](https://docs.github.com/en/rest/branches/branch-protection).
