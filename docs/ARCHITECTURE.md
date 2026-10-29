# Arquitetura e decisões

Consolidação As-Built da Entrega 3: 20/10/2026, Issue #21. O mapa de arquivos, esquema SQLite e configuração efetiva estão em [AS_BUILT.md](AS_BUILT.md). Os ADRs abaixo continuam válidos; não houve troca de arquitetura de produção.

O ReservaLab separa as regras de negócio da comunicação HTTP e da persistência. Isso permite testar conflitos e datas com um relógio fixo e verificar os contratos da API usando um servidor local e bancos temporários.

```mermaid
flowchart LR
    Cliente[Cliente HTTP] --> HTTP[Adaptador HTTP]
    HTTP --> Servico[Serviço de reservas]
    Servico --> Validacao[Validação e relógio]
    Servico --> Repo[Repositório SQLite]
    Repo --> Banco[(Arquivo SQLite)]
    Testes[Harness automatizado] --> HTTP
    Testes --> Servico
    Testes --> Repo
```

As decisões abaixo foram propostas durante a preparação assistida por IA. A aprovação humana deve ser registrada no PR. Alterações posteriores devem atualizar a decisão afetada e a especificação correspondente.

## ADR-001 — Python e biblioteca padrão

**Contexto:** a entrega precisa de uma aplicação pequena e de testes fáceis de reproduzir.

**Decisão:** aceitar Python 3.12 ou superior, padronizar Python 3.13 no contêiner e usar servidor HTTP da biblioteca padrão, `sqlite3` e `unittest`, sem dependências Python externas. O runtime local inicialmente disponível é Python 3.12.14.

**Consequências:** instalação curta e execução offline da suíte após obter o runtime. O servidor serve para demonstração local; autenticação, exposição pública e operação em produção exigem outra avaliação. Não há interface gráfica no escopo.

## ADR-002 — SQLite e transação única para reservas

**Contexto:** verificar o horário livre e inserir em operações separadas permitiria que duas requisições aprovassem a mesma vaga.

**Decisão:** persistir em SQLite e executar a consulta de conflito e a inserção dentro de uma mesma transação `BEGIN IMMEDIATE`. Cada operação deve usar conexão apropriada ao seu ciclo de vida, sem compartilhar uma conexão de forma insegura entre requisições.

**Consequências:** a escrita serializada garante o invariante no processo de reserva. A opção é adequada ao exercício, com poucos usuários e um banco local; não constitui arquitetura distribuída.

## ADR-003 — UTC e intervalos semiabertos

**Contexto:** textos com fusos distintos podem representar o mesmo instante; períodos adjacentes não devem bloquear um ao outro.

**Decisão:** exigir fuso explícito, validar instantes de minuto inteiro, armazenar/comparar em UTC e retornar UTC com `Z`. Definir horários como `[início, fim)`.

**Consequências:** comparação determinística e adjacência permitida. O cliente é responsável por converter para o horário local de exibição. Segundos diferentes de zero são rejeitados para evitar ambiguidade na duração.

## ADR-004 — Cancelamento preserva o registro

**Contexto:** apagar a reserva tornaria a consulta e a repetição de pedidos menos previsíveis.

**Decisão:** mudar `active` para `cancelled`, preservando o registro. Repetir o cancelamento retorna o registro cancelado e status 200.

**Consequências:** a listagem mostra o histórico simples e o horário fica livre. Esta entrega não mantém trilha completa de auditoria nem identifica quem cancelou.

## ADR-005 — Relógio e banco substituíveis nos testes

**Contexto:** testes com o relógio real ou banco compartilhado podem falhar apenas pela passagem do tempo ou pela ordem de execução.

**Decisão:** permitir injeção de relógio e uso de arquivos SQLite temporários isolados. Testar tanto as regras diretamente quanto requisições HTTP reais contra servidor de teste.

**Consequências:** cenários de passado, igualdade e concorrência podem ser reproduzidos. O teste do adaptador não substitui o teste das regras nem o inverso.

## ADR-006 — Entrega por PR e evidência autêntica

**Contexto:** a atividade avalia colaboração, revisão e validação, além do código.

**Decisão:** usar `main`, `develop` e `feature/*`; integrar por PR revisado por outro integrante. Registrar tarefas em Issues com um responsável humano e um revisor. O uso de IA é identificado, sem atribuir a agentes a identidade de colegas.

**Consequências:** decisões e comentários ficam rastreáveis. Aprovações, merges e submissões dependem dos integrantes. A disponibilidade de proteção de branch deve ser conferida nas configurações do repositório, e não presumida pela existência deste documento.

## ADR-007 - Cobertura de linhas com biblioteca padrão

**Contexto:** a Entrega 3 exige evidência de cobertura das unidades críticas, enquanto as anteriores comprovaram apenas passagem dos testes.

**Decisão:** executar o harness real sob trace do CPython, com escopo explícito em todos os arquivos da aplicação, threads instrumentadas e denominador das tabelas de linha do bytecode excluindo docstrings. Relatar fontes ausentes/não importados e hashes. Agregado crítico: domain, service, repository e server.

**Consequências:** não há nova dependência da aplicação ou dos testes. A métrica não é cobertura de branches, subprocessos externos ou bibliotecas nativas. Não foi definido percentual mínimo pelo enunciado; 100% de linhas não comprova todos os caminhos. O relatório preserva eventuais linhas ausentes.

## ADR-008 - Release e documento gerados a partir de evidência final

**Contexto:** PDFs de preparação ficaram desatualizados quando PRs foram integrados. A Entrega 3 exige link real de release e vídeo, ainda inexistentes no início da preparação.

**Decisão:** manter uma prévia explicitamente marcada e gerar o PDF definitivo junto à release, a partir dos logs/cobertura do commit final de main e do link real informado pela equipe. O workflow manual verifica main protegida/atual, nenhum PR aberto, homologação humana declarada e tag v1.0.0 ainda inexistente; testa antes de publicar. Arquivos são anexados e recebem checksums.

**Consequências:** a publicação depende de ações humanas reais e de permissões do GitHub. ReportLab é dependência apenas documental. O workflow não faz commit direto, não altera proteções e não confirma duração/acesso do vídeo sozinho. Falhas após criação de um rascunho exigem inspecionar o estado antes de retomar; tag estável não é sobrescrita.
