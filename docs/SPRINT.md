# Sprint inicial — escopo e tarefas

Objetivo: entregar uma API pequena de reserva de salas, sua especificação, ambiente reproduzível, harness funcional e evidências de colaboração. A preparação inicial pode ser auxiliada por IA; cada responsável deve conferir e assumir sua contribuição em atividade identificável no GitHub.

Esta tabela deve ser espelhada em Issues. Os códigos `E1-*` são identificadores de planejamento, não números de Issues do GitHub. A existência de um item nesta tabela não significa que a Issue foi encerrada ou a contribuição humana concluída.

| ID | Tarefa independente | Responsável | Revisor | Entregável e aceite | Dependência |
| --- | --- | --- | --- | --- | --- |
| E1-01 | Conferir repositório e governança | Áquila | Gabriel | Repositório acessível, `main`/`develop`/`feature/*`, Issues, instruções e regras de PR verificadas. | Nenhuma |
| E1-02 | Revisar especificação SDD | Gabriel | Pedro | Contratos e RF/RN/RNF conferidos; comentário com exemplos reais e refinamentos registrados quando necessários. | Nenhuma |
| E1-03 | Validar regras e persistência | Pedro | Eduardo | Conflito, adjacência, cancelamento, durações, persistência e concorrência comprovados; correções via PR se necessárias. | Contrato inicial disponível |
| E1-04 | Reproduzir ambiente e harness | Eduardo | Áquila | Execução independente documentada, casos de borda conferidos e logs reais vinculados. | Implementação e ambiente disponíveis |
| E1-05 | Revisar fluxo de IA e contexto | Áquila | Gabriel | `AGENTS.md`, prompts e limites do auxílio de IA correspondem ao trabalho efetuado. | Nenhuma |
| E1-06 | Consolidar refinamentos | Gabriel | Pedro | Cada mudança tem motivo, responsável, requisito e evidência; validações humanas são identificadas como tais. | E1-02 e feedback disponível |
| E1-07 | Revisar pipeline e evidências | Eduardo | Áquila | Check do commit revisado aprovado; link/artefato acessível e coerente com o README. | E1-04 |
| E1-08 | Consolidar entrega e PDF | Áquila | Gabriel | Nomes/RAs, URL, ambiente, IA, comandos e prints/logs presentes; pendências humanas tratadas antes da submissão. | E1-01 a E1-07 |

## Fluxo das branches

```text
main                 versão de entrega aprovada
  └── develop        integração da sprint
       ├── feature/revisao-especificacao
       ├── feature/validacao-reservas
       ├── feature/harness-evidencias
       └── feature/documentacao-entrega
```

Os nomes das branches de contribuição são exemplos para os integrantes; conferir no GitHub quais branches já existem antes de criar uma. O PR de preparação inicial também deve ser revisado por uma pessoa do grupo. Nenhuma branch nominal, por si só, comprova contribuição de um membro.

Cada PR deve descrever o problema, requisitos afetados, alteração resultante, comandos executados e resultado. Mudanças de contrato exigem atualizar a especificação e os testes no mesmo PR, ou explicitar a dependência. O revisor deve conferir o commit final após ajustes relevantes. O PR de `develop` para `main` só pode ser integrado depois da revisão entre integrantes e aprovação do pipeline.

## Organização sugerida no GitHub

- **A fazer:** Issue criada e critérios claros.
- **Em andamento:** integrante assumiu a tarefa e registrou sua branch ou análise.
- **Em revisão:** PR ou evidência disponível e revisor solicitado.
- **Concluído:** critérios cumpridos, revisão registrada e merge realizado quando houver alteração.

As Issues satisfazem o registro de divisão de tarefas; um quadro GitHub Projects é opcional quando as Issues já mostram o escopo, responsáveis e dependências.

## Limite do escopo

Ficam fora desta sprint: autenticação, frontend, e-mails, agenda recorrente, integração institucional e implantação pública do serviço. A prioridade é entregar as regras e sua validação sem aumentar a complexidade do projeto.
