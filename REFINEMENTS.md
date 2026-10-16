# Referência de concorrência

O registro consolidado de refinamentos está em [docs/REFINEMENTS.md](docs/REFINEMENTS.md).

Este arquivo foi introduzido no PR #10, com referência à validação do PR #11. A expressão original "bloqueando a tabela" foi corrigida na Entrega 2: `BEGIN IMMEDIATE` inicia uma transação de escrita e serializa escritores no SQLite; não cria um bloqueio por tabela. A consulta de conflito e a inserção ocorrem na mesma transação, conforme RN-10 e ADR-002.

A explicação é consistente com a [documentação do SQLite](https://www.sqlite.org/lang_transaction.html). Não houve alteração da implementação de persistência.
