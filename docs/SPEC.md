# Especificação técnica — ReservaLab

Versão: 1.0 · Entrega 1 · Estado: contrato para implementação e revisão humana.

## 1. Problema e objetivo

Grupos de estudantes precisam reservar salas de estudo sem disputar o mesmo espaço no mesmo horário. O ReservaLab oferece uma API HTTP pequena para consultar salas, criar e listar reservas e cancelar uma reserva. O núcleo da entrega é a validação de conflitos e de limites de uso, com testes reproduzíveis.

O sistema é uma demonstração acadêmica local. A identificação do estudante é apenas um nome informado pelo cliente. Não há autenticação, autorização por usuário, interface web, notificações, pagamentos, recorrência, gestão de salas ou integração com a agenda real da instituição nesta entrega. A listagem e o cancelamento são acessíveis a qualquer cliente que alcance o serviço; portanto, não se devem inserir dados pessoais reais nem disponibilizar esta versão como serviço público de reservas.

## 2. Vocabulário e modelo

| Conceito | Definição |
| --- | --- |
| Sala | Recurso fixo com identificador, nome e capacidade. |
| Reserva ativa | Reserva que impede outra reserva sobreposta para a mesma sala. |
| Reserva cancelada | Registro preservado para consulta que não bloqueia a sala. |
| Intervalo | Período semiaberto `[starts_at, ends_at)`: inclui o início e exclui o fim. |
| Relógio | Dependência usada para determinar o instante atual, substituível nos testes. |

Catálogo inicial: Sala 1 (`id=1`, capacidade 4) e Sala 2 (`id=2`, capacidade 8).

Uma reserva contém `id` UUID, `room_id`, `student_name`, `starts_at`, `ends_at`, `participants` e `status`. Os estados possíveis são `active` e `cancelled`. A transição permitida é `active → cancelled`; cancelar novamente retorna o mesmo registro cancelado. Não há reativação ou edição de reserva.

## 3. Requisitos funcionais

| ID | Requisito | Critério de aceitação |
| --- | --- | --- |
| RF-01 | Consultar a disponibilidade operacional. | `GET /health` retorna 200 e `{"status":"ok"}`. |
| RF-02 | Consultar o catálogo de salas. | `GET /rooms` retorna 200, com as duas salas e suas capacidades. |
| RF-03 | Criar uma reserva. | Um pedido válido e livre retorna 201, com UUID e estado `active`. |
| RF-04 | Listar reservas. | `GET /bookings` retorna 200 e uma lista que inclui reservas ativas e canceladas; inicialmente a lista é vazia. |
| RF-05 | Impedir sobreposição. | Duas reservas ativas para a mesma sala não podem compartilhar nenhum instante; o pedido conflitante retorna 409. |
| RF-06 | Cancelar uma reserva. | `DELETE /bookings/{id}` retorna 200 e o registro com estado `cancelled`; libera o horário e é idempotente. |
| RF-07 | Informar erros de entrada e de protocolo. | Entradas inválidas não geram registros e retornam o código HTTP definido no contrato. |
| RF-08 | Persistir reservas. | Reabrir o repositório sobre o mesmo arquivo SQLite preserva os registros e seus estados. |

## 4. Regras de negócio

| ID | Regra |
| --- | --- |
| RN-01 | A sala deve existir no catálogo inicial. Um identificador inteiro positivo sem sala correspondente retorna 404, inclusive se exceder o intervalo de 64 bits do SQLite. |
| RN-02 | `student_name` deve ser texto Unicode válido em UTF-8; após remover espaços nas extremidades, deve ter entre 2 e 100 caracteres, inclusive. O nome normalizado é persistido. Substitutos Unicode isolados são rejeitados com 400. |
| RN-03 | `room_id` e `participants` devem ser inteiros JSON positivos; booleanos não são aceitos como inteiros. Tipos incorretos e valores não positivos retornam 400. |
| RN-04 | `participants` deve estar entre 1 e a capacidade da sala, inclusive. |
| RN-05 | Datas devem ser strings ISO 8601 com fuso explícito (`Z` ou deslocamento `±HH:MM`, horas de `00` a `23`, minutos de `00` a `59`). A precisão é de minuto inteiro: segundos e frações devem representar zero. As respostas normalizam o instante para UTC, com segundos e sufixo `Z`. |
| RN-06 | O início deve ser maior ou igual ao instante retornado pelo relógio da aplicação no momento da criação. |
| RN-07 | A duração deve estar entre 30 e 120 minutos, inclusive. O fim deve ser posterior ao início. Não há limite de antecedência nesta entrega. |
| RN-08 | Há conflito quando `novo_inicio < fim_existente` e `novo_fim > inicio_existente`, considerando apenas a mesma sala e reservas ativas. |
| RN-09 | Reservas adjacentes são permitidas: terminar às 11h e começar às 11h não é conflito. Horários iguais em salas diferentes são permitidos. |
| RN-10 | A verificação de conflito e a inserção devem ocorrer na mesma transação de escrita para impedir duplicação por solicitações simultâneas. |
| RN-11 | Cancelar uma reserva inexistente retorna 404. Repetir o cancelamento de uma existente retorna 200, sem criar outro registro. |
| RN-12 | O corpo de criação contém exatamente os cinco campos de entrada. Campos ausentes ou desconhecidos, inclusive `id` e `status`, são rejeitados com 400. |

## 5. Requisitos não funcionais

| ID | Requisito verificável |
| --- | --- |
| RNF-01 | Executar com Python 3.12 ou superior e biblioteca padrão, sem banco externo nem dependências Python de terceiros em produção. O contêiner padroniza Python 3.13. |
| RNF-02 | Disponibilizar ambiente em contêiner e alternativa local, com os mesmos testes. A versão de Python deve ser explícita no ambiente padronizado. |
| RNF-03 | Executar testes sem internet e sem dados reais. Cada teste deve isolar seus dados e não depender da ordem da suíte. |
| RNF-04 | Permitir substituir o relógio e o arquivo de banco para que testes não dependam de datas reais ou de um banco compartilhado. |
| RNF-05 | Limitar corpos de criação a 16 KiB; rejeitar excesso com 413 e tipo de mídia diferente de JSON com 415. |
| RNF-06 | Retornar erros como JSON legível, sem expor rastreamentos internos ao cliente. |
| RNF-07 | Registrar evidências reais de execução do harness e executar a suíte no GitHub Actions em PRs. Uma falha deve resultar em código de saída diferente de zero. |
| RNF-08 | Alterações em `main` e integração em `develop` devem ocorrer por PR, com revisão de outra pessoa registrada antes do merge. |

Não há meta de latência, escala, SLA ou cobertura percentual definida. A entrega comprova comportamento funcional em testes; não comprova desempenho em produção.

## 6. Contratos HTTP

As rotas usam JSON UTF-8. Na criação, enviar `Content-Type: application/json`; parâmetros usuais como `charset=utf-8` podem acompanhar o tipo. Os exemplos abaixo são ilustrativos. As datas da criação devem ser ajustadas para o futuro quando executadas manualmente.

As constantes `NaN`, `Infinity` e `-Infinity` não são JSON válido para este contrato e retornam 400, com código `invalid_json`.

### Consulta operacional e catálogo

`GET /health` → **200**

```json
{"status": "ok"}
```

`GET /rooms` → **200**

```json
{"rooms": [{"id": 1, "name": "Sala 1", "capacity": 4}, {"id": 2, "name": "Sala 2", "capacity": 8}]}
```

### Criação

`POST /bookings` → **201**

```json
{
  "room_id": 1,
  "student_name": "Estudante Exemplo",
  "starts_at": "2099-09-10T10:00:00-03:00",
  "ends_at": "2099-09-10T11:00:00-03:00",
  "participants": 3
}
```

Resposta ilustrativa:

```json
{
  "id": "3f1ce746-2b77-4cde-82d1-7f9faf7d0b4c",
  "room_id": 1,
  "student_name": "Estudante Exemplo",
  "starts_at": "2099-09-10T13:00:00Z",
  "ends_at": "2099-09-10T14:00:00Z",
  "participants": 3,
  "status": "active"
}
```

| Campo de entrada | Tipo | Restrições |
| --- | --- | --- |
| `room_id` | inteiro | 1 ou 2; não aceita booleano. |
| `student_name` | string | 2 a 100 caracteres após normalização. |
| `starts_at` | string | ISO 8601, fuso explícito, minuto inteiro, início não passado. |
| `ends_at` | string | ISO 8601, fuso explícito, minuto inteiro, duração de 30 a 120 minutos. |
| `participants` | inteiro | 1 até a capacidade da sala; não aceita booleano. |

### Listagem e cancelamento

`GET /bookings` → **200**, objeto `{"bookings": [...]}`. Cada item tem o formato da resposta de criação. Sem reservas, retorna `{"bookings": []}`. A ordenação não é garantia de contrato; consumidores não devem depender dela.

`DELETE /bookings/{id}` → **200**, objeto de reserva com `status: "cancelled"`. Não exige corpo. O identificador é o UUID recebido na criação. Um identificador sem registro correspondente retorna 404.

### Respostas de erro

| Código | Situação |
| --- | --- |
| 400 | JSON inválido, corpo que não seja objeto, campos ausentes/desconhecidos, tipos ou regras de validação inválidos. |
| 404 | Sala ou reserva inexistente; caminho não reconhecido. |
| 405 | Método não suportado para uma rota conhecida. |
| 409 | Sobreposição com reserva ativa da mesma sala. |
| 413 | Corpo de criação maior que 16 KiB. |
| 415 | Tipo de mídia de criação diferente de `application/json`. |

Erros retornam o formato `{"error": {"code": "codigo_estavel", "message": "Descrição legível."}}`. Por exemplo, sobreposição usa `booking_conflict` e reserva inexistente usa `booking_not_found`. Se vários campos estiverem inválidos simultaneamente, o cliente não deve depender da ordem da validação nem de uma mensagem textual específica. Métodos recusados nas rotas conhecidas também retornam o cabeçalho `Allow`.

Na criação, `Content-Length` deve informar o tamanho do corpo. Ausência, valor inválido e uso de `Transfer-Encoding` são rejeitados com 400. A lista de métodos tratada pelo adaptador é GET, POST, DELETE, PUT, PATCH, HEAD, OPTIONS e TRACE; métodos fora dessa lista podem receber a resposta padrão do servidor. HEAD não retorna corpo.

## 7. Decomposição em unidades testáveis

| Unidade | Responsabilidade | Entrada/saída e isolamento |
| --- | --- | --- |
| Modelo e validação (`reservalab/domain.py`) | Normalizar valores e aplicar RN-02 a RN-07 e RN-12. | `validate_payload(payload, now)` → dicionário normalizado ou `DomainError`. Sem HTTP. |
| Serviço de reservas (`reservalab/service.py`) | Coordenar casos de uso, validação e persistência. | `BookingService(db_path, now)` expõe `list_rooms`, `create_booking`, `list_bookings` e `cancel_booking`. |
| Repositório SQLite (`reservalab/repository.py`) | Catálogo, capacidade, conflito, esquema e gravação atômica. | `BookingRepository(db_path)` → registros ou erro de domínio; banco temporário isolado nos testes. |
| Adaptador HTTP (`reservalab/server.py`) | Rotas, métodos, leitura limitada do corpo e conversão de erros. | `create_server(db_path, host, port, now)` → servidor configurado; requisições → status e JSON. |
| Harness (`scripts/run_tests.py`) | Descobrir e executar cenários, resumir resultados e produzir evidências. | Suíte → código de saída, `tests.log` e `summary.json` no diretório escolhido. |

## 8. Plano de validação e rastreabilidade

A tabela define os cenários mínimos a conferir na suíte e os requisitos que justificam cada cenário. Ela é um plano de aceitação; a evidência efetiva de execução está nos relatórios gerados pelo harness e nos checks dos PRs.

| ID de cenário | Cenário | Requisitos |
| --- | --- | --- |
| CT-01 | Saúde, catálogo e listagem inicialmente vazia. | RF-01, RF-02, RF-04 |
| CT-02 | Criar reserva válida, UUID, estado ativo e nome sem espaços externos. | RF-03, RN-02 |
| CT-03 | Limites de duração: 30 e 120 aceitos; 29 e 121 rejeitados. | RN-07 |
| CT-04 | Capacidade: mínimo 1 e capacidade total aceitos; zero e excesso rejeitados. | RN-04 |
| CT-05 | Ausência, campo extra, booleanos, tipo incorreto e nome fora dos limites. | RF-07, RN-02, RN-03, RN-12 |
| CT-06 | Sem fuso, data inválida, segundos não zero e início passado rejeitados; início igual ao relógio aceito. | RN-05, RN-06, RNF-04 |
| CT-07 | Fusos diferentes para o mesmo instante produzem UTC equivalente e detectam conflito. | RN-05, RN-08 |
| CT-08 | Sobreposição parcial, contida, envolvente e exatamente igual é rejeitada. | RF-05, RN-08 |
| CT-09 | Adjacência antes/depois e mesmo horário em salas diferentes são aceitos. | RN-09 |
| CT-10 | Cancelamento libera o horário, preserva a listagem e pode ser repetido. | RF-04, RF-06, RN-11 |
| CT-11 | Sala/reserva inexistente retorna 404. | RN-01, RN-11 |
| CT-12 | Registros persistem após reabrir o banco. | RF-08 |
| CT-13 | Duas criações simultâneas conflitantes resultam em apenas uma reserva. | RN-10 |
| CT-14 | HTTP real: status, JSON, mídia inválida, excesso de corpo, método e rota inválidos. | RF-07, RNF-05, RNF-06 |
| CT-15 | Harness termina com falha quando um teste falha e CI publica resultado verificável. | RNF-07 |

## 9. Critério de conclusão da Entrega 1

Repositório acessível ao professor, branches e PR de entrega publicados, ambiente e harness executáveis, documentação consistente e evidências reais disponíveis. A participação humana exige que cada integrante execute sua tarefa, deixe revisão/comentário autêntico e realize a submissão no Moodle. Esses atos não podem ser substituídos por texto gerado ou atribuídos ao grupo antes de acontecerem.
