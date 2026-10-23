"""Gera PDF de encerramento a partir de evidências reais; ReportLab é só documental."""

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, TableStyle


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/herethere04/reservalab-sdd"


def academic_team():
    """Usa a identificação acadêmica autorizada no README, sem duplicar os dados."""
    team = []
    for line in (ROOT / "README.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 2 and re.fullmatch(r"\d{8}", cells[1]):
                team.append(cells[:2])
    if len(team) != 4:
        raise ValueError("Conferir os quatro nomes e RAs da tabela acadêmica no README.")
    return team


def validate_video_url(value):
    parsed = urlsplit(value)
    host = (parsed.hostname or "").lower()
    allowed = host in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be",
                       "drive.google.com", "docs.google.com", "loom.com", "www.loom.com"}
    allowed = allowed or host == "sharepoint.com" or host.endswith(".sharepoint.com")
    if parsed.scheme != "https" or not allowed or parsed.username or parsed.password:
        raise ValueError("Informe o link HTTPS real do vídeo no YouTube, Drive, Loom ou SharePoint.")
    return value


def load_evidence(folder):
    report = json.loads((folder / "coverage.json").read_text(encoding="utf-8"))
    tests = json.loads((folder / "tests" / "summary.json").read_text(encoding="utf-8"))
    if not tests["success"] or tests["tests_run"] < 1 or any(tests[key] for key in ["failures", "errors", "skipped"]):
        raise ValueError("O PDF de encerramento exige suíte aprovada e sem testes ignorados.")
    for row in report["modules"]:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError(f"Evidência desatualizada para {row['path']}; executar cobertura novamente.")
    if report["tests"]["tests_run"] != tests["tests_run"]:
        raise ValueError("Relatórios de testes e cobertura não correspondem à mesma execução.")
    for name, expected in tests["source_snapshot"]["files"].items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Fonte alterado após os testes: {name}; executar cobertura novamente.")
    return report, tests


def build(output, evidence, tests, video_url, commit, draft):
    fonts = Path(reportlab.__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("Report", str(fonts / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont("ReportBold", str(fonts / "VeraBd.ttf")))
    pdfmetrics.registerFontFamily("Report", normal="Report", bold="ReportBold")
    navy, teal = colors.HexColor("#172D46"), colors.HexColor("#087B85")
    styles = {
        "title": ParagraphStyle("title", fontName="ReportBold", fontSize=27, leading=33, textColor=navy, spaceAfter=12),
        "subtitle": ParagraphStyle("subtitle", fontName="Report", fontSize=13, leading=19, textColor=navy, spaceAfter=18),
        "h": ParagraphStyle("h", fontName="ReportBold", fontSize=13, leading=18, textColor=navy, spaceBefore=14, spaceAfter=8, keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Report", fontSize=9.1, leading=13.8, textColor=navy, spaceAfter=8),
        "cell": ParagraphStyle("cell", fontName="Report", fontSize=7.8, leading=11, textColor=navy),
        "head": ParagraphStyle("head", fontName="ReportBold", fontSize=7.8, leading=11, textColor=colors.white),
        "small": ParagraphStyle("small", fontName="Report", fontSize=7.8, leading=11.5, textColor=navy, spaceAfter=7),
    }
    story = []

    def p(text, style="body"):
        story.append(Paragraph(html.escape(str(text)), styles[style]))

    def link(label, url):
        story.append(Paragraph(f'<b>{html.escape(label)}</b><br/><link href="{html.escape(url, quote=True)}" color="#087B85"><u>{html.escape(url)}</u></link>', styles["body"]))

    def table(headers, rows, widths):
        cells = [[Paragraph(html.escape(str(value)), styles["head" if index == 0 else "cell"])
                  for value in row] for index, row in enumerate([headers, *rows])]
        obj = LongTable(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
        obj.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), navy),
                                 ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F5F7")]),
                                 ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#D5E0E5")),
                                 ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                 ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
        story.extend([obj, Spacer(1, 10)])

    def heading(text):
        p(text, "h")

    release_url = REPOSITORY + "/releases/tag/v1.0.0"
    story.append(Spacer(1, 44))
    p("BOOTCAMP III / ETAPA FINAL", "h")
    p("ReservaLab", "title")
    p("Entrega 3 - Solução final, testes aprovados e release versionada", "subtitle")
    p("Turma B - 0726 - Campus Virtual - 2026/2. Prazo: 25/10/2026, às 23h55 (Brasília).")
    table(["Integrante", "RA"], academic_team(), [385, 114])
    link("Repositório público", REPOSITORY)
    if draft:
        heading("DOCUMENTO DE PREPARAÇÃO - NÃO SUBMETER")
        p("As evidências técnicas foram geradas, mas a homologação final, a release v1.0.0 e o vídeo da equipe ainda precisam ser concluídos. Este arquivo não declara a entrega encerrada.")
    else:
        link("Release oficial v1.0.0", release_url)
        link("Vídeo da demonstração funcional", video_url)
    p("Preparação técnica e redação assistidas pelo Codex. A equipe real está identificada acima; nenhuma revisão, gravação ou submissão pessoal é presumida.", "small")
    story.append(PageBreak())

    heading("1. Resumo executivo de encerramento")
    p("O ReservaLab atende ao problema de grupos de estudantes disputarem uma mesma sala no mesmo horário. A solução entregue é uma API HTTP local que consulta duas salas, cria/lista reservas, impede sobreposição, permite cancelamento idempotente e preserva os dados em SQLite. O contrato funcional definido na Entrega 1 foi mantido.")
    p(f"A execução identificada neste documento aprovou {tests['tests_run']} de {tests['tests_run']} testes, com zero falhas, erros e ignorados. A cobertura de linhas das unidades críticas foi {evidence['critical']['percent']}%; a aplicação completa teve {evidence['total']['percent']}%. Passagem dos testes e cobertura são métricas distintas e não certificam ausência de defeitos.")
    p("A Entrega 3 consolida a especificação As-Built, melhora a evidência de testes de protocolo/CLI, mede cobertura e prepara empacotamento e publicação versionada. Não foram acrescentados frontend, autenticação ou serviços externos. A aplicação serve à demonstração acadêmica local; uso institucional exigiria novos requisitos e avaliação de segurança.")

    heading("2. Versão, procedência e release")
    p(f"Identificador da aplicação: 1.0.0. Commit de referência: {commit or 'não informado'}. As evidências registram o estado e os hashes dos fontes efetivamente testados; uma árvore modificada não é atribuída integralmente ao commit-base.")
    p(f"HEAD registrado pelo harness: {tests['git']['head'] or 'indisponível na imagem, pois .git não é copiado'}. Working tree dirty: {tests['git']['working_tree_dirty']}. UTC da execução: {tests['timestamp_utc']}.", "small")
    p(f"Manifesto SHA-256: {tests['source_snapshot']['manifest_sha256']} ({tests['source_snapshot']['file_count']} arquivos medidos).", "small")
    if draft:
        p("Release prevista: v1.0.0. Ela não é apresentada como publicada neste documento de preparação. A publicação depende da integração revisada em main e do vídeo real informado pela equipe.")
    else:
        link("Link direto da release oficial", release_url)
        p("A release reúne o pacote de fontes, este PDF, evidências de testes/cobertura e arquivo de checksums. O fluxo verifica main protegida, commit atual, ausência de PRs abertos, tag ainda não existente e declaração humana de homologação antes de publicar.")

    heading("3. Especificação definitiva e arquitetura As-Built")
    p("Fluxo real: cliente HTTP -> adaptador HTTP -> serviço -> validação do domínio -> repositório SQLite -> resposta JSON. O serviço recebe um relógio substituível nos testes; cada operação abre sua conexão SQLite. A consulta de conflito e a inserção usam a mesma transação BEGIN IMMEDIATE.")
    table(["Componente", "Contrato entregue"], [
        ["Domínio", "Campos exatos; nome UTF-8 válido; inteiros sem booleanos; fuso explícito; minuto inteiro; início não passado; duração 30-120 min."],
        ["Persistência", "Duas salas (capacidades 4 e 8), reservas ativas/canceladas, UUID, UTC, índice por sala/estado/intervalo. Cancelamento preserva o registro."],
        ["HTTP", "GET /health, GET /rooms, GET/POST /bookings e DELETE /bookings/{id}. Sucessos 200/201; erros 400/404/405/409/413/415 conforme a SPEC."],
        ["Concorrência", "Conflito quando novo início < fim existente e novo fim > início existente; apenas reservas ativas da mesma sala. Intervalos adjacentes permitidos."],
        ["Ambiente", "Python >=3.12, biblioteca padrão, SQLite; imagem Python 3.13.7. Sem variáveis obrigatórias da aplicação; CLI configura host/port/db/version."],
    ], [100, 399])
    link("SDD As-Built e contratos detalhados", REPOSITORY + "/blob/" + ("feature/entrega-3-final" if draft else "v1.0.0") + "/docs/AS_BUILT.md")
    p("Trade-offs defendidos nos ADRs: biblioteca padrão reduz instalação; SQLite serializa escritores; UTC e intervalos semiabertos simplificam comparação; cancelamento lógico preserva histórico simples; relógio/banco substituíveis isolam testes; PRs e revisão humana tornam a aceitação rastreável.")

    heading("4. Execução real dos testes e cobertura")
    table(["Dado", "Resultado observado"], [
        ["Ambiente", f"CPython {tests['python']} / {tests['platform']}"],
        ["Suíte", f"{tests['tests_run']} executados, {tests['failures']} falhas, {tests['errors']} erros, {tests['skipped']} ignorados; sucesso: {tests['success']}"],
        ["Tempo do harness", f"{tests['elapsed_seconds']} s nesta execução (não é benchmark)."],
        ["Instrumentação", "trace do CPython; eventos de linha, incluindo threads criadas durante a suíte; denominador das tabelas de linha do bytecode, excluindo docstrings."],
    ], [115, 384])
    rows = []
    for row in evidence["modules"]:
        percent = f"{row['percent']:.2f}%" if row["percent"] is not None else "sem linhas"
        rows.append([row["path"], f"{row['covered_lines']}/{row['executable_lines']}", percent,
                     ", ".join(map(str, row["missing_lines"])) or "nenhuma"])
    table(["Módulo", "Linhas", "Cobertura", "Ausentes"], rows, [230, 65, 75, 129])
    p(f"Agregado crítico (domain, repository, service e server): {evidence['critical']['covered_lines']}/{evidence['critical']['executable_lines']} linhas, {evidence['critical']['percent']}%. Aplicação inteira: {evidence['total']['covered_lines']}/{evidence['total']['executable_lines']} linhas, {evidence['total']['percent']}%.")
    p("Não se mede cobertura de branches, SQLite nativo, bibliotecas externas ou subprocessos de fixtures. Módulos não executados entram no denominador. O relatório HTML e os arquivos anotados mostram hits e linhas ausentes; os JSON/logs permitem conferir contagem, ambiente e hashes. Mesmo 100% de linhas não garante testar todos os caminhos ou requisitos.")
    log = (Path(tests['_evidence_dir']) / "tests" / "tests.log").read_text(encoding="utf-8")
    excerpt = [line for line in log.splitlines() if line.startswith("Ran ") or line == "OK" or line.startswith("FAILED")]
    p("Trecho do log real: " + " | ".join(excerpt), "small")
    p("Cenários: limites/validação de reservas, sobreposição, adjacência, UTC, persistência e concorrência; ciclo HTTP real, protocolo inválido e HEAD; encerramento/versão da CLI; sucesso/falha/erro/suíte vazia do harness; cobertura que inclui código ausente e preserva falhas; demonstração HTTP executável.")

    story.append(PageBreak())
    heading("5. Empacotamento e guia de execução")
    p("Após obter a versão publicada, executar localmente: python -m reservalab. Configuração opcional: --host 127.0.0.1 --port 8000 --db data/reservalab.db. A aplicação não exige chave de API, credencial ou variável de ambiente.")
    p("Comandos únicos do ambiente padronizado: docker compose up --build -d api; docker compose run --build --rm tests; docker compose run --build --rm coverage. A API é exposta em loopback e o banco é mantido no volume booking-data. O primeiro build requer obter a imagem. Parar com docker compose down preserva esse volume.")
    p("Alternativa local de testes: python scripts/run_tests.py --output-dir evidence/latest. Cobertura: python scripts/run_coverage.py --output-dir evidence/coverage. Relatório: evidence/coverage/index.html. Demonstração descartável: python scripts/demo.py. A geração do PDF usa dependência documental separada e não altera a instalação da API.")
    p("Limitações assumidas: http.server não é recomendado para produção; sem TLS próprio, autenticação/autorização, limitação de requisições, SLA, teste de carga ou política institucional de retenção. Usar dados fictícios na demonstração.")

    heading("6. Demonstração funcional e retrospectiva")
    if video_url:
        link("Vídeo de 3 a 5 minutos informado pela equipe", video_url)
    else:
        p("Vídeo ainda não gravado/publicado. Eduardo recebeu a tarefa na Issue #24; o roteiro de 3min40s e o comando de demonstração estão em docs/DEMO.md. Este campo precisa do URL real antes da submissão.")
    p("O roteiro mostra catálogo, criação 201, conflito 409, cancelamento, liberação do horário e capacidade 400. A execução dos testes/cobertura deve ocorrer durante a gravação, sem apresentar um log antigo como execução ao vivo. O banco de demonstração é temporário e usa dados fictícios.")
    p("O histórico das entregas evidenciou desafios em UTC, validação estrita de JSON/Unicode, concorrência SQLite e coerência entre a documentação e o estado dos PRs. A Entrega 3 acrescentou testes de protocolo e CLI e relatórios verificáveis de cobertura. A lição de governança foi conferir o commit, a revisão e o merge efetivo, pois um checklist isolado pode ficar desatualizado.")
    p("A equipe informou uso somente do Codex. O auxílio observável foi estruturar especificações, preparar código/testes, identificar casos de borda e organizar evidências/documentação. Não houve baseline controlada sem IA nem registro de tempo que sustente percentual de produtividade. O ganho sustentado é a existência desses artefatos verificáveis; a contribuição de cada integrante deve ser confirmada por seus registros reais.")
    p("A revisão humana continua central. Riscos: código alucinado/inseguro, ações destrutivas, exposição de contexto/dados, origem/licenças de trechos e dependência da ferramenta. Controles usados: escopo limitado, fontes e logs reais, dados fictícios, hashes, testes e PRs revisados. A aprovação e a defesa acadêmica são responsabilidades humanas.")

    story.append(PageBreak())
    heading("7. Conferência dos cinco itens de submissão")
    table(["Exigência", "Evidência neste documento"], [
        ["Release oficial", "Seção 2 e link direto da release v1.0.0; pendente na preparação, resolvido no PDF gerado pela publicação oficial."],
        ["Nome completo e RA", "Quatro integrantes identificados na capa com os dados reais autorizados."],
        ["Testes e cobertura", "Seção 4: números reais, metodologia, módulos, log e hashes; arquivos completos nos anexos da release."],
        ["Vídeo funcional", "Seção 6: link real após gravação/publicação pela equipe; não preenchido artificialmente."],
        ["Resumo e lições", "Seções 1 e 6: escopo, resultado, limites, uso real de IA e aprendizados sem métricas inventadas."],
    ], [135, 364])
    if draft:
        p("Pendências para encerrar: revisão/homologação da proposta; integração revisada em main; gravação/publicação do vídeo; execução do fluxo Release final v1.0.0 com o link do vídeo; conferência do PDF definitivo anexado à release e envio pela Sala Online. Não foi comprovada submissão nesta preparação.")
    else:
        p("Antes do envio acadêmico, conferir abertura deste PDF e acesso aos links da release e do vídeo. Os arquivos finais são os anexos da release; enviar pela Sala Online conforme orientação do professor. A publicação não comprova por si o envio no ambiente da disciplina.")

    heading("8. Referências e rastreabilidade")
    for label, suffix in [("Issue central da Entrega 3", "/issues/21"), ("Gabriel - As-Built e PDF", "/issues/22"),
                          ("Pedro - testes, cobertura e empacotamento", "/issues/23"), ("Eduardo - vídeo e release", "/issues/24"),
                          ("PR #15 - integração da Entrega 2", "/pull/15"), ("PR #19 - revisão documental", "/pull/19"),
                          ("PR #20 - promoção documental para main", "/pull/20")]:
        link(label, REPOSITORY + suffix)
    p("Fontes acadêmicas: enunciado completo da Entrega 3 (duas páginas, consultado em 20/10/2026) e entregas anteriores. Fontes técnicas: código, SPEC, AS_BUILT, ARCHITECTURE, refinamentos, logs e relatórios gerados nesta execução. Não foram inventadas entrevistas, reuniões, aprovações ou gravações.", "small")

    def chrome(canvas, doc):
        canvas.saveState()
        canvas.setFont("ReportBold", 7)
        canvas.setFillColor(teal)
        canvas.drawString(48, A4[1] - 31, "RESERVALAB / ENTREGA FINAL")
        canvas.setFont("Report", 7)
        canvas.drawRightString(A4[0] - 48, A4[1] - 31, "PREPARAÇÃO" if draft else "RELEASE v1.0.0")
        canvas.setStrokeColor(colors.HexColor("#D5E0E5"))
        canvas.line(48, A4[1] - 40, A4[0] - 48, A4[1] - 40)
        canvas.line(48, 44, A4[0] - 48, 44)
        canvas.setFont("Report", 6.8)
        canvas.drawString(48, 31, "Documento acadêmico - preparação assistida pelo Codex")
        canvas.drawRightString(A4[0] - 48, 31, str(doc.page))
        canvas.restoreState()

    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=48, rightMargin=48, topMargin=57, bottomMargin=58,
                            title="ReservaLab - Entrega 3", author="Equipe ReservaLab; preparação assistida pelo Codex")
    doc.build(story, onFirstPage=chrome, onLaterPages=chrome)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--video-url")
    parser.add_argument("--commit")
    parser.add_argument("--draft", action="store_true", help="Marca explicitamente preparação não submetível")
    args = parser.parse_args()
    if not args.draft and (not args.video_url or not args.commit or not re.fullmatch(r"[0-9a-f]{40}", args.commit)):
        parser.error("PDF final exige link real do vídeo e SHA de 40 caracteres do commit da release.")
    video = validate_video_url(args.video_url) if args.video_url else None
    evidence, tests = load_evidence(args.evidence_dir.resolve())
    tests["_evidence_dir"] = str(args.evidence_dir.resolve())
    build(args.output.resolve(), evidence, tests, video, args.commit or tests["git"]["head"], args.draft)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
