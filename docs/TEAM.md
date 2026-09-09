# Equipe, contribuições e revisão

| Integrante | RA | Responsabilidade inicial | Revisado por |
| --- | --- | --- | --- |
| Áquila de Brito Barbosa | 22453948 | Integração, governança, execução final e PDF de submissão. | Gabriel Ferreira Costa |
| Gabriel Ferreira Costa | 22450586 | Conferência da especificação e dos contratos de entrada/saída. | Pedro Ivo Gonçalves Pinheiro Coelho |
| Pedro Ivo Gonçalves Pinheiro Coelho | 22453629 | Conferência das regras de reserva, persistência e concorrência. | Eduardo Cabral Nunes |
| Eduardo Cabral Nunes | 22454089 | Conferência do ambiente, harness, casos de borda e evidências. | Áquila de Brito Barbosa |

Os nomes acima identificam responsabilidades propostas; não comprovam trabalho já realizado. E-mails e credenciais não precisam constar no repositório público. Os nomes de usuário do GitHub devem ser associados às Issues depois que cada integrante aceitar o acesso. O responsável é informado no texto da Issue mesmo enquanto a atribuição formal estiver pendente.

## Primeiro acesso de cada integrante

1. Abrir o repositório e aceitar o convite, caso exista. Informar seu usuário GitHub a Áquila para habilitar colaboração e atribuição de Issues.
2. A implementação inicial está em `feature/entrega-inicial`, em PR com base `develop`. Enquanto esse PR aguarda revisão humana, selecionar essa branch para ler e executar o projeto; `develop` ainda não contém a implementação completa.
3. Clonar, selecionar `feature/entrega-inicial`, ler `README.md`, `AGENTS.md` e `docs/SPEC.md` e conferir sua Issue.
4. Executar o harness e anexar à Issue ou ao PR o resultado real, incluindo data, versão do Python e eventuais falhas.
5. Revisar o PR inicial no escopo atribuído. Gabriel confere contratos e documentação; Pedro confere regras e persistência; Eduardo confere ambiente, testes e evidências. Áquila coordena e responde aos comentários, sem aprovar seu próprio PR.
6. Depois da revisão humana e do merge do PR inicial em `develop`, criar branches `feature/<assunto-curto>` a partir de `develop` para as correções ou refinamentos necessários. Abrir PRs e solicitar a revisão circular indicada na tabela.

Para conferir o PR inicial antes de seu merge:

```sh
git clone https://github.com/herethere04/reservalab-sdd.git
cd reservalab-sdd
git switch feature/entrega-inicial
python scripts/run_tests.py --output-dir evidence/latest
```

Após o merge inicial, exemplo para uma contribuição que realmente exija alteração:

```sh
git fetch origin
git switch develop
git pull --ff-only
git switch -c feature/revisao-especificacao
# editar e conferir o diff
python scripts/run_tests.py --output-dir evidence/latest
git add docs/SPEC.md
git commit -m "docs: revisar contratos da especificacao"
git push -u origin feature/revisao-especificacao
```

Abra o PR no GitHub com base `develop`. Não faça commits em `main`, não envie credenciais e não use `git add .` sem conferir os arquivos incluídos.

O commit mínimo de inicialização é a origem compartilhada das referências de governança. Isso não representa commits de implementação feitos diretamente em `main`. O histórico e os PRs devem mostrar a entrada da implementação somente pelo fluxo de revisão.

Para iniciar a API local, use `python -m reservalab --db data/reservalab.db`. O README contém também as opções do ambiente padronizado em contêiner.

## O que cada pessoa deve fazer

### Áquila

- Conferir se os quatro integrantes e RAs estão corretos no README e PDF.
- Habilitar acesso dos colegas, conferir Issues e regras de branch e acompanhar o escopo da sprint.
- Executar a aplicação e o harness seguindo apenas o README; registrar qualquer ajuste necessário em sua branch.
- Revisar o PR de Eduardo: repetir o comando em ambiente limpo e verificar se logs e documentação correspondem ao resultado observado.
- Após as revisões humanas e checks obrigatórios, coordenar os merges autorizados e o PR de `develop` para `main`. Atualizar o PDF com o link de evidência definitivo e disponibilizá-lo aos colegas.

### Gabriel

- Ler `docs/SPEC.md` e comparar o contrato com respostas reais da API e testes.
- Conferir limites de nome, capacidade, datas com fuso, campos extras e semântica de cancelamento.
- Se houver divergência, registrar o caso reproduzível, propor uma correção na especificação ou no comportamento, justificar a escolha e atualizar `docs/REFINEMENTS.md`.
- Abrir seu PR ou registrar uma revisão detalhada com evidências se a especificação não exigir mudanças; não criar alteração sem necessidade apenas para produzir um commit.
- Revisar a contribuição de Áquila e verificar nomes, referências, governança e clareza dos comandos.

### Pedro

- Conferir a fórmula de sobreposição e executar casos de inclusão, igualdade, adjacência e salas diferentes.
- Confirmar que cancelar libera o período, que os registros sobrevivem à reabertura do banco e que a escrita concorrente preserva uma única reserva conflitante.
- Corrigir problemas encontrados em uma branch própria e acrescentar testes ligados aos requisitos afetados. Registrar os resultados na Issue.
- Revisar o PR de Gabriel, confrontando os ajustes de especificação com a implementação.

### Eduardo

- Reproduzir o ambiente descrito no README e executar o harness; executar também o ambiente em contêiner quando houver Docker disponível.
- Conferir JSON inválido, mídia inadequada, limite do corpo, métodos/rotas inválidos e isolamento dos bancos temporários.
- Verificar os artefatos e logs do GitHub Actions e registrar a execução efetivamente observada. Se Docker não estiver disponível, registrar essa limitação; não declarar uma execução que não ocorreu.
- Corrigir a documentação ou os testes quando necessário e abrir PR com a evidência.
- Revisar o PR de Pedro, repetindo especialmente os testes de concorrência e cancelamento.

## Como registrar um code review válido

O revisor deve usar sua própria conta GitHub, ler o diff, executar os comandos pertinentes e comentar ao menos o que verificou, o resultado e eventuais ajustes pedidos. Use **Request changes** quando houver problema material. Use **Approve** apenas após verificar que o PR atende à especificação. Uma pessoa não aprova seu próprio PR.

Um comentário útil descreve o procedimento real: requisito conferido, entrada usada, resultado obtido e eventual divergência. Comentários genéricos e aprovações produzidas em nome dos colegas não comprovam colaboração.

A atividade exige revisão entre membros antes do merge; não exige inventar quatro aprovações no mesmo PR. O PR inicial precisa de aprovação autêntica de pelo menos outro integrante, além dos checks e da quantidade de aprovações configurada no repositório. Todos devem registrar sua própria contribuição, seja uma conferência técnica reproduzível, um refinamento justificado ou uma correção necessária. Se não houver defeito, documente a verificação; não fabrique problemas, commits ou resultados anteriores.

## Definição de concluído

- Tarefa vinculada a uma Issue com escopo claro e responsável.
- Código e documentação coerentes com os IDs da especificação.
- Harness aprovado e resultado real anexado ou vinculado.
- PR sem dados sensíveis, revisado por outro integrante e com pedidos de alteração resolvidos.
- Merge pela interface do GitHub após os checks e a aprovação exigida.
- Issue encerrada e evidência final acessível aos professores.

Cada integrante deve submeter no Moodle o mesmo PDF final. A entrega do arquivo por uma pessoa não substitui a submissão dos demais.
