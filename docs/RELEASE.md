# Publicação oficial v1.0.0 e PDF definitivo

Responsável pela conferência/publicação: eddyocn (#24); revisor: Claneeer (#23). A preparação técnica não cria uma release oficial nem uma aprovação humana.

## Condições antes de publicar

1. Gabriel confere As-Built/relatório e registra revisão real; Pedro homologa testes, cobertura e reprodução.
2. Integrar a proposta em develop e promover para main por PR revisado, com check harness aprovado para o commit final. Não desativar proteção nem fazer push direto.
3. Resolver todos os PRs da entrega; o workflow exige nenhum PR aberto no repositório.
4. Eduardo grava/publica o vídeo de 3 a 5 minutos e confere o acesso do professor. O link tem que ser real, no YouTube, Drive, Loom ou SharePoint.
5. Confirmar que main protegida contém exatamente a versão homologada e que não existe tag/release v1.0.0 anterior.

## Publicar pelo GitHub (sem comandos de infraestrutura)

1. Abrir a aba **Actions** do repositório depois da integração em main.
2. Selecionar **Release final v1.0.0** e clicar **Run workflow**.
3. Escolher **main**, inserir o link HTTPS do vídeo e marcar a confirmação somente se a homologação e o acesso do professor realmente foram conferidos.
4. Executar e acompanhar o resultado. O fluxo valida as condições, produz evidências e publica a tag/release sobre o commit testado.
5. Abrir `https://github.com/herethere04/reservalab-sdd/releases/tag/v1.0.0`; conferir o commit, os anexos e o vídeo. Baixar o PDF **ReservaLab_Entrega_3.pdf**, abrir e conferir os cinco itens da submissão.
6. Gabriel/eddyocn conferem o PDF final e disponibilizam o mesmo arquivo ao grupo para envio conforme a orientação da disciplina. Não enviar a prévia marcada PREPARAÇÃO.

O checkbox do workflow é uma declaração humana, não substitui uma revisão registrada nos PRs. A duração e o acesso ao vídeo precisam ser conferidos por uma pessoa; um URL aceito pelo gerador não certifica essas condições.

## Anexos esperados

- ReservaLab_Entrega_3.pdf, com link direto da release, integrantes/RAs, testes/cobertura, vídeo e resumo executivo/retrospectiva.
- ReservaLab-1.0.0-source.zip, criado por git archive do commit final.
- tests.log e summary.json da execução final real.
- coverage.json, coverage.md e ZIP com HTML/fontes anotados.
- AS_BUILT.md, RELEASE_NOTES.md e SHA256SUMS.txt.

O pacote inclui o código da aplicação e os materiais rastreáveis. A prévia de preparação é excluída do git archive. Nunca sobrescrever silenciosamente uma tag estável. Se falhar após criar uma release em rascunho, verificar as evidências e o estado do rascunho antes de qualquer ação manual; não declarar a publicação concluída pelo simples início do workflow.

## Geração documental manual (alternativa)

Se o workflow não estiver disponível, um integrante autorizado pode executar o gerador em ambiente documental com ReportLab, apontando para evidências do commit final e vídeo reais, publicar a release via GitHub e anexar os arquivos. Isso não dispensa os critérios de revisão, checks, main protegida, tag correta e acesso ao vídeo.

A preparação de 20/10 não publica v1.0.0 antecipadamente sobre a branch da proposta. O endereço previsto não é evidência de uma release que ainda não existe.
