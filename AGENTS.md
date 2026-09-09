# Instruções para agentes - ReservaLab

## Contexto

Entrega acadêmica inicial: API simples de reservas de salas. Python >=3.12,
biblioteca padrão, SQLite e unittest; Docker usa Python 3.13.7.
Leia docs/SPEC.md e docs/ARCHITECTURE.md antes de alterar código.

## Fluxo SDD

1. Identifique a issue e os IDs dos requisitos afetados.
2. Se o contrato mudar, atualize primeiro a SPEC e registre a motivação em docs/REFINEMENTS.md.
3. Crie ou ajuste testes observáveis para os critérios de aceite.
4. Implemente a menor mudança que satisfaça os testes.
5. Execute `python scripts/run_tests.py` e reporte o resultado real.
6. Abra PR de feature/* para develop; promoção develop para main exige revisão humana.

## Restrições

- Não fazer commits nem pushes diretos em main ou develop após a inicialização.
- Nunca inventar aprovações, autoria de colegas, logs, cobertura ou resultados.
- Não alterar testes para esconder um erro; reconciliar com a especificação.
- Datas conscientes de fuso, UTC na persistência e intervalos [início, fim).
- Consulta de conflito e inserção precisam da mesma transação SQLite.
- Não adicionar serviços externos, autenticação ou interface web nesta entrega.
- Usar dados fictícios nos exemplos e nos testes; não incluir segredos no Git.
- A IA pode revisar tecnicamente, mas a aprovação da equipe deve ser real.

## Validação

Local: `python scripts/run_tests.py --output-dir evidence/latest`
Contêiner: `docker compose run --build --rm tests`
Execução: `python -m reservalab`
