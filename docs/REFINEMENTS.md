# Registro de refinamentos da especificação

Este registro distingue decisões de preparação assistida por IA de feedback humano. Não houve, até a redação inicial deste arquivo, reunião ou aprovação do grupo documentada aqui. Os registros RFN-001 a RFN-005 são esclarecimentos feitos durante a elaboração do contrato; não são apresentados como resultado de testes ou revisão de colegas.

| ID | Origem | Ambiguidade inicial | Refinamento adotado | Requisitos afetados |
| --- | --- | --- | --- | --- |
| RFN-001 | Análise do agente durante a especificação | “Horário de reserva” não dizia como comparar clientes em fusos diferentes. | Exigir fuso explícito, normalizar em UTC e responder com `Z`. | RN-05, CT-07 |
| RFN-002 | Análise do agente durante a especificação | Um horário poderia conter segundos e produzir limites de duração pouco claros. | Exigir instantes de minuto inteiro; testar as fronteiras 30/120 e rejeições 29/121. | RN-05, RN-07, CT-03, CT-06 |
| RFN-003 | Análise do agente durante a especificação | “Conflito” poderia proibir dois grupos consecutivos. | Usar intervalos `[início, fim)`; permitir fim de uma reserva igual ao início da seguinte. | RN-08, RN-09, CT-08, CT-09 |
| RFN-004 | Análise do agente durante a especificação | Uma consulta de conflito seguida de inserção separada permitiria corrida. | Verificar conflito e inserir na mesma transação `BEGIN IMMEDIATE`; incluir cenário simultâneo. | RN-10, CT-13 |
| RFN-005 | Análise do agente durante a especificação | “Cancelar” não definia exclusão nem comportamento em repetição. | Preservar registro como `cancelled`, liberar o horário e tornar a operação idempotente. | RN-11, CT-10 |

## Feedback de implementação e testes

Em 09/09/2026, a revisão técnica entre agentes encontrou os casos abaixo e orientou correções de validação. São resultados da revisão assistida por IA, ainda sujeitos à conferência dos integrantes. As correções preservam os comportamentos centrais do contrato e tornam explícitos casos de entrada que a primeira versão não detalhava.

| ID | Problema reproduzido antes da correção | Decisão e refinamento | Testes de regressão | Requisitos |
| --- | --- | --- | --- | --- |
| RFN-006 | O parser de datas do Python aceitava deslocamento `+00:60` e o normalizava como `+01:00`, embora os minutos do deslocamento fossem inválidos. | Validar a gramática do fuso antes da conversão: minutos de `00` a `59`. Rejeitar esses deslocamentos com 400 e `invalid_datetime`. | `test_invalid_timezone_offset_minutes_are_rejected`, em `tests/test_service.py`. | RN-05, CT-06 |
| RFN-007 | Um identificador positivo de sala maior que o intervalo de inteiros de 64 bits produzia `OverflowError` na associação de parâmetros do SQLite. | Consultar a existência do identificador no catálogo antes de usá-lo como parâmetro inteiro no banco. Um inteiro positivo sem sala correspondente retorna 404 e `room_not_found`, inclusive fora do intervalo de 64 bits. | `test_room_id_above_sqlite_integer_range_is_not_found`, em `tests/test_service.py`; `test_enormous_unknown_room_id_is_a_client_error`, em `tests/test_http.py`. | RN-01, RN-03, CT-11, CT-14 |
| RFN-008 | Um nome com substituto Unicode isolado, como `\ud800`, passava pela contagem de caracteres e falhava ao ser codificado para gravação no SQLite. | Validar que o nome pode ser codificado em UTF-8 antes da persistência. Entrada inválida retorna 400 e `invalid_student_name`. | `test_unpaired_surrogate_in_student_name_is_rejected`, em `tests/test_service.py`; `test_unpaired_unicode_surrogate_is_a_client_error`, em `tests/test_http.py`. | RN-02, RNF-06, CT-05, CT-14 |
| RFN-009 | O decodificador JSON padrão do Python aceita as constantes não finitas `NaN`, `Infinity` e `-Infinity`, que não pertencem ao contrato JSON da API. | Recusar constantes não finitas durante a decodificação do corpo, com 400 e `invalid_json`, antes da validação de campos. | `test_nonfinite_json_numbers_are_rejected`, em `tests/test_http.py`. | RF-07, RNF-06, CT-14 |

### Evidência depois das correções

A suíte foi executada no ambiente local Windows com CPython **3.12.14**, em **2026-09-09 às 16:35:58 UTC**. Resultado: **46 testes, 0 falhas, 0 erros, 0 ignorados**, em 9,199 segundos. A evidência desta execução é local; não comprova execução em Docker ou GitHub Actions.

Comando:

```sh
python scripts/run_tests.py --output-dir evidence/post-review-local
```

Arquivos: [log completo](../evidence/post-review-local/tests.log) e [resumo JSON](../evidence/post-review-local/summary.json). Os seis métodos citados na tabela estão incluídos no log aprovado. O resumo registra um manifesto SHA-256 do conjunto de 15 arquivos de aplicação, testes e ambiente:

```text
be4777520fd0a01952ff573d13c90d34b94d8164944866cdfd386776b366c8eb
```

Nesta execução o projeto ainda não tinha um commit Git próprio identificado pelo harness; por isso `git.head` está nulo. O manifesto vincula a evidência aos arquivos medidos. Logs futuros do CI devem acrescentar a referência do commit executado.

Novos registros devem indicar o caso observado, resultado anterior, decisão, requisito e evidência após o ajuste. Quando o teste revela defeito de implementação e o contrato já está claro, deve-se corrigir a implementação e preservar o contrato.

## Feedback do grupo

**Pendente de revisão humana.** Cada integrante deve registrar o comentário e o link do PR/Issue correspondente. Uma validação sem mudança também pode ser documentada, desde que descreva o que foi conferido e a evidência real.

Modelo de registro a preencher:

```text
ID: RFN-010
Autor e origem: <integrante ou agente; revisão/teste específico>
Requisito afetado: <RF/RN/RNF>
Problema observado: <entrada, saída e expectativa>
Decisão: <ajuste do contrato, correção da implementação ou manutenção justificada>
Evidência: <link do PR/Issue e teste/log>
Revisor humano: <nome e link; ou pendente>
```
