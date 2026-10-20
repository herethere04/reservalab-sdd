# ReservaLab 1.0.0 - SDD As-Built

Consolidação técnica de 20/10/2026, Issue #21. Versão técnica: 1.0.0. O estado de homologação e publicação é comprovado pelos PRs e pela release; o identificador no código não substitui a tag oficial no GitHub.

## Escopo entregue

API HTTP JSON local de reservas de duas salas de estudo. Resolve criação, consulta, conflito de intervalos, cancelamento e persistência. Sem interface web, autenticação, autorização por proprietário, notificações ou integração institucional. A versão é pronta para demonstração acadêmica local; não é serviço institucional de produção.

## Componentes e dependências reais

| Componente | Arquivo | Responsabilidade |
| --- | --- | --- |
| Versão e CLI | reservalab/__init__.py e __main__.py | Identificador 1.0.0, argumentos host/port/db/version; fechamento do servidor em interrupção/erro. |
| Domínio | reservalab/domain.py | Validação de campos, datas conscientes de fuso, minutos inteiros, duração e normalização UTC. |
| Serviço | reservalab/service.py | Casos de uso e relógio injetável; delegação à persistência. |
| Persistência | reservalab/repository.py | SQLite, catálogo, restrições e transação BEGIN IMMEDIATE unindo conflito/inserção. |
| Adaptador HTTP | reservalab/server.py | ThreadingHTTPServer, JSON UTF-8, limite de 16 KiB, rotas e status da SPEC. |
| Harness | scripts/run_tests.py | unittest, exit code, testes/log/resumo com ambiente e manifesto SHA-256. |
| Cobertura | scripts/run_coverage.py | trace do CPython, incluindo threads criadas durante a suíte; JSON, Markdown, HTML e fontes anotados. |
| Demonstração | scripts/demo.py | Oito etapas HTTP reais com banco temporário, dados fictícios e resposta verificada. |

Runtime: Python >=3.12; imagem fixa python:3.13.7-slim-bookworm; biblioteca padrão e SQLite da distribuição Python. Nenhuma dependência Python externa na aplicação, testes ou medição de cobertura. A geração documental usa ReportLab 4.4.9 em ambiente separado.

## Persistência efetiva

`rooms(id INTEGER PRIMARY KEY, name TEXT NOT NULL, capacity INTEGER NOT NULL CHECK(capacity > 0))`.

`bookings(id TEXT PRIMARY KEY, room_id INTEGER NOT NULL REFERENCES rooms(id), student_name TEXT NOT NULL, starts_at TEXT NOT NULL, ends_at TEXT NOT NULL, participants INTEGER NOT NULL CHECK(participants > 0), status TEXT NOT NULL CHECK(status IN ('active','cancelled')))`. Índice `bookings_room_interval(room_id, status, starts_at, ends_at)`.

Salas iniciais: 1/capacidade 4 e 2/capacidade 8, inseridas com INSERT OR IGNORE. A conexão ativa foreign_keys=ON e timeout de 10 segundos. Cada operação abre/fecha a própria conexão; bancos :memory: são recusados. Criação e cancelamento usam transação de escrita BEGIN IMMEDIATE. Datas são strings UTC comparáveis; não há armazenamento de identidade autenticada ou trilha completa de auditoria.

## API, erros e regras definitivas

| Método/rota | Sucesso | Outras respostas previstas |
| --- | --- | --- |
| GET /health | 200, status ok | 405 para método tratado não permitido. |
| GET /rooms | 200, catálogo | 405 para método tratado não permitido. |
| POST /bookings | 201, reserva ativa com UUID | 400 validação/JSON/protocolo; 404 sala; 409 conflito; 413 corpo grande; 415 mídia. |
| GET /bookings | 200, lista de ativas/canceladas | 405 para método tratado não permitido. |
| DELETE /bookings/{id} | 200, reserva cancelada | 404 inexistente; 405 método tratado não permitido. |

Campos exatos de criação: room_id, student_name, starts_at, ends_at, participants. Não aceita booleano no lugar de inteiro. Nome UTF-8 válido com 2-100 caracteres após trim; duração 30-120 minutos; início >= relógio atual; capacidade da sala; fuso explícito e minuto inteiro. Cancelamento repetido é idempotente e libera o período. Intervalos [início,fim): adjacência permitida; só reservas ativas da mesma sala conflitam.

Erros retornam objeto error/code/message. HEAD nas rotas tratadas retorna 405 e cabeçalho Allow, sem corpo. Métodos fora da lista tratada podem receber a resposta padrão do http.server. Não se promete resposta JSON para toda falha operacional inesperada. Contratos completos e rastreabilidade RF/RN/CT: [SPEC.md](SPEC.md).

## Configuração e execução

CLI: --host (127.0.0.1), --port (8000), --db (data/reservalab.db), --version. Não existem variáveis de ambiente obrigatórias da aplicação. O Docker define apenas PYTHONDONTWRITEBYTECODE/PYTHONUNBUFFERED. Compose expõe o serviço em loopback e persiste o SQLite em volume booking-data. Portas/arquivo podem ser configurados pelos argumentos CLI ou pelo comando do serviço.

Comandos e reprodução estão no README. `docker compose up --build -d api` inicia a API; `docker compose run --build --rm tests` executa o harness; `docker compose run --build --rm coverage` mede cobertura. Alternativa local sem dependências externas: python -m reservalab / scripts/run_tests.py / scripts/run_coverage.py.

## Evidências e limites

A preparação inicial em main 5be5482 passou em 50/50 testes. As lacunas de protocolo/CLI e de emissão de cobertura são verificadas na suíte ampliada da Entrega 3. Números finais estão nos logs e em coverage.json; não se copiam porcentagens de outra execução.

A cobertura usa o conjunto de linhas do bytecode compilado, excluindo docstrings, e eventos de linha efetivamente executados. Mede todos os módulos da aplicação, inclusive os não importados. Domínio, serviço, repositório e HTTP formam o agregado crítico. Não mede branches, SQL nativo, código externo nem subprocessos de fixtures. Todos os percentuais dependem da versão do Python e dos fontes identificados por hash.

As limitações de produção permanecem: http.server não recomendado para produção, sem TLS próprio/autenticação/autorização/rate limit, sem política institucional de retenção, sem garantia de carga/latência/recuperação. Testes e cobertura não certificam ausência de defeitos. ADRs e trade-offs: [ARCHITECTURE.md](ARCHITECTURE.md).
