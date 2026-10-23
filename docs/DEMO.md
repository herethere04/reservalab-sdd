# Vídeo da Entrega 3 - roteiro de 3 a 5 minutos

Responsável pela gravação/publicação: **eddyocn**, Issue #24. Revisor: Claneeer. O usuário informou em 20/10 que o vídeo ainda não existe. Este roteiro e o script não substituem o vídeo real da equipe.

## Preparar e gravar

1. Obter a versão homologada do projeto e Python 3.12 ou superior.
2. Abrir um terminal com fonte legível e o gravador de tela da preferência da equipe. Mostrar a tela da aplicação/terminal; usar narração própria ou participação real dos integrantes.
3. Mostrar `python -m reservalab --version` e o commit com `git rev-parse HEAD`.
4. Executar `python scripts/demo.py --pause 6`. O script inicia um servidor HTTP real em porta local livre, usa um banco temporário e valida as respostas. Não depende de configuração de infraestrutura nem altera o banco do projeto.
5. Durante a gravação, executar `python scripts/run_coverage.py --output-dir evidence/video`. Mostrar o término do harness, quantidade de testes, zero falhas/erros e percentuais de cobertura realmente obtidos. Abrir `evidence/video/index.html` para a tabela dos módulos.
6. Publicar o vídeo e testar o acesso pelo professor. Registrar o link na Issue #24 para uso na release e no PDF.

Em máquinas com `python3`, substituir `python`. Um resultado que falhou deve ser investigado; não usar um log antigo para simular testes ao vivo.

## Sequência sugerida (3min40s)

| Tempo | Mostrar | Explicar com suas próprias palavras |
| --- | --- | --- |
| 0:00-0:25 | Título ReservaLab, versão e commit | Problema: dois grupos disputando a mesma sala no mesmo horário. Solução: API de reservas com validação de conflito. |
| 0:25-1:40 | `demo.py`: catálogo, criação 201, conflito 409, cancelamento, nova reserva, capacidade 400 | SQLite persiste o estado; apenas reservas ativas bloqueiam o horário, e o cancelamento preserva histórico. |
| 1:40-2:35 | Comando de cobertura/harness executado de verdade e relatório HTML | Percentual de passagem dos testes é diferente de cobertura de linhas. Mostrar os valores da execução gravada. |
| 2:35-3:10 | SPEC/As-Built e diagrama do README | Domínio, serviço, HTTP e SQLite; UTC; transação única; limites de uma demonstração local sem autenticação. |
| 3:10-3:40 | Release/PRs e retrospectiva | Codex ajudou em especificação/testes/documentação; revisão humana verificou o resultado. Não houve medição controlada de ganho de produtividade. |

Pode ajustar a duração para ficar entre 3 e 5 minutos. Não é necessário usar os mesmos textos palavra por palavra. Não atribuir fala ou execução a integrante que não participou.

## Antes de entregar o link

- Duração entre 3:00 e 5:00, vídeo e voz legíveis, sem segredos ou dados pessoais desnecessários na tela.
- Exibe o fluxo funcional e a execução dos testes em tempo real.
- Publicação no YouTube (não listado serve), Drive, Loom ou SharePoint, com permissão para o professor.
- Verificar em janela sem sessão privada ou com outra conta autorizada. Se houver login institucional obrigatório, explicar o acesso ao professor.
- Informar o URL definitivo; não usar um link fictício ou uma pasta vazia.
