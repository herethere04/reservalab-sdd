# Uso de IA no fluxo SDD

## Ferramenta e participação

A preparação inicial utilizou Codex no aplicativo desktop, com agentes paralelos para tarefas delimitadas de implementação, testes e documentação. Trata-se de auxílio de geração e revisão de artefatos. Os agentes não são integrantes do grupo, não representam contas dos colegas e não fornecem as aprovações humanas exigidas pela atividade.

O registro de revisão humana e de execução independente deve ser preenchido pelos integrantes nas Issues e PRs. Não se presume que um colega leu, executou ou aprovou conteúdo apenas porque seu nome aparece como responsável planejado.

## Ordem de trabalho SDD

1. Ler `AGENTS.md`, `docs/SPEC.md` e os ADRs antes de alterar comportamento.
2. Identificar os requisitos e cenários de aceitação da tarefa.
3. Se o contrato for ambíguo, propor o refinamento e registrar a justificativa em `docs/REFINEMENTS.md`.
4. Implementar a menor unidade capaz de cumprir o contrato e preservar os limites entre HTTP, serviço e banco.
5. Criar ou ajustar testes que verifiquem comportamento observável, incluindo os limites relevantes.
6. Executar o harness; corrigir falhas e conferir o relatório real.
7. Conferir o diff, atualizar documentação e abrir PR vinculado à Issue.
8. Obter revisão de outro integrante e aprovação dos checks antes do merge.

## Contexto persistente

`AGENTS.md` é o arquivo de instruções do agente no repositório. Ele deve manter a especificação como referência, restringir mudanças ao escopo, exigir evidências reais e preservar o fluxo de branches. A especificação define o comportamento; os testes verificam esse comportamento. Um agente não deve alterar ambos apenas para esconder uma falha sem justificar a mudança no contrato.

## Prompts reutilizáveis

Os exemplos abaixo são modelos para próximas interações, e não transcrições literais de todas as mensagens usadas na preparação.

**Implementação de uma unidade:**

> Leia AGENTS.md, docs/SPEC.md e docs/ARCHITECTURE.md. Implemente somente a tarefa da Issue informada, em branch feature. Cite os requisitos afetados, preserve os contratos HTTP e escreva testes de comportamento para os limites relevantes. Execute o harness e relate o resultado efetivo, sem declarar sucesso para comandos que não executou.

**Refinamento da especificação:**

> Compare o contrato da especificação com a implementação e a suíte. Mostre divergências concretas com entradas e resultados. Proponha o menor ajuste necessário e registre em docs/REFINEMENTS.md sua motivação e origem. Não atribua a decisão ao grupo sem uma revisão humana registrada.

**Revisão auxiliar:**

> Revise o diff deste PR procurando regressões em conflito de horários, UTC, validação, cancelamento e atomicidade SQLite. Aponte somente problemas sustentados pelo código ou por reprodução. Esta análise auxilia o revisor humano e não deve ser apresentada como aprovação de um integrante.

## Como repetir o uso

Abra a pasta clonada no Codex, confirme que a ferramenta pode ler `AGENTS.md` e associe a solicitação à Issue em andamento. Informe a branch de trabalho e o requisito que deseja implementar ou conferir. Leia cada alteração antes de enviar o PR. O runtime de IA não é necessário para executar a aplicação ou a suíte, e não se deve incluir token, chave de API ou arquivo de sessão no repositório.

O comando do harness é `python scripts/run_tests.py --output-dir evidence/latest`; ele produz log textual e resumo JSON. O servidor local pode ser iniciado com `python -m reservalab --db data/reservalab.db`.

## Evidências e limites

Os commits, diffs, logs do harness e checks no GitHub documentam os artefatos e validações técnicas. As Issues e revisões em contas individuais documentam a participação humana. Ao relatar uma execução, informar o comando, ambiente, data e resultado observado. Se um ambiente não foi executado, registrar a limitação explicitamente.
