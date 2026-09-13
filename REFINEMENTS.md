## Revisão de Especificação - Concorrência

* **Motivo:** Necessidade de garantir a integridade do banco de dados SQLite quando múltiplas reservas tentam ser criadas exatamente ao mesmo tempo, evitando conflitos de sala.
* **Requisito:** O sistema deve suportar concorrência e isolamento adequado, bloqueando a tabela durante inserções críticas (uso do `BEGIN IMMEDIATE`).
* **Teste:** Execução do Test Harness validando a regra de concorrência e testes de isolamento de banco.
* **Link:** (Registro validado no Pull Request #11)
