# Refinamentos da Entrega 3

## RFN-018 - Cobertura observável (Issue #21, RNF-09, CT-16)

O enunciado final exige cobertura, ainda não medida nas entregas anteriores. Acrescenta-se um comando que executa o harness real sob `trace` da biblioteca padrão e relata linhas executáveis/hit/missing por módulo. A linha executável vem das tabelas de linhas do bytecode, com docstrings excluídas; não se mede cobertura de branches, subprocessos externos, banco SQLite nativo ou biblioteca padrão. Os quatro módulos críticos são domínio, serviço, repositório e adaptador HTTP. Não foi definido percentual mínimo pelo professor.

## RFN-019 - Consolidação As-Built e release (RNF-10/11, CT-18)

O contrato HTTP não muda. A documentação passa a descrever exatamente a versão entregue, os comandos, os limites e a diferença entre servidor local e serviço institucional. A release final exige main protegida e homologada, nenhuma pendência de PR da entrega e vídeo real acessível. Um relatório de preparação não se apresenta como release publicada.

## RFN-020 - Demonstração e evidências humanas (CT-17)

O vídeo ainda não existe na preparação inicial de 20/10, conforme informado pelo usuário. Eduardo recebe gravação/publicação, retrospectiva e conferência documental na Issue #24; nenhuma tarefa de infraestrutura de contêiner lhe foi atribuída. As tarefas humanas de validação/revisão permanecem distintas da preparação assistida pelo Codex.

## RFN-021 - Identificador da versão (RNF-10, CT-17)

O cabeçalho Server ainda dizia ReservaLab/0.1. Para coerência com o candidato v1.0.0, a versão passa a ser definida em `reservalab.__version__`, exibida no cabeçalho HTTP e na opção CLI `--version`. A existência desse identificador não significa que a tag/release já foi publicada. Rotas, campos e regras de reserva permanecem preservados.

## RFN-022 - Marcadores sem linha no CPython 3.13 (RNF-09, CT-16)

A primeira execução padronizada passou em 64 testes, mas o pós-processamento da cobertura falhou: `dis.findlinestarts` no Python 3.13 pode produzir `None` para instruções sem linha associada, e a comparação com zero levantou TypeError. A medição local em 3.12 não revelou essa diferença. A correção ignora exclusivamente marcadores sem linha de fonte; não exclui linhas reais nem altera testes para melhorar percentuais. O fixture de módulo não importado foi ampliado com uma classe, exercitando o caso na versão padronizada. O log da tentativa foi preservado em evidence/entrega3-coverage-compatibility.
