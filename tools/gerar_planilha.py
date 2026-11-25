"""Gera conteudo-portfolio.xlsx (planilha modelo) a partir do array PADRAO do index.html.

Uso (na raiz do repositório):
    pip install openpyxl
    python tools/gerar_planilha.py
"""
import json
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"
SAIDA = RAIZ / "conteudo-portfolio.xlsx"

COLUNAS = ["tipo", "titulo", "detalhe", "descricao", "tags", "link", "arquivo", "miniatura", "mostrar"]
LARGURAS = {"tipo": 18, "titulo": 40, "detalhe": 45, "descricao": 70, "tags": 30,
            "link": 40, "arquivo": 26, "miniatura": 26, "mostrar": 12}

# tipo, onde aparece, colunas que usa
TIPOS = [
    ("perfil", "Caixa Jogadora 1 (nome e classe)", "titulo = nome; detalhe = linha de classe"),
    ("ficha", "Ficha da Jogadora 1 (até 3 itens)", "titulo = rótulo; detalhe = valor"),
    ("sobre", "Aba SOBRE MIM (um parágrafo por linha)", "descricao"),
    ("destaque", "Aba SOBRE MIM, quadradinhos de destaque", "titulo = rótulo; detalhe = valor"),
    ("formacao", "Aba CURRÍCULO, caixa Formação", "titulo, detalhe"),
    ("experiencia", "Aba CURRÍCULO, caixa Experiência", "titulo, detalhe"),
    ("programa", "Aba CURRÍCULO, caixa Programas e iniciativas", "titulo, detalhe"),
    ("ferramenta", "Aba CURRÍCULO, etiquetas de Ferramentas e temas", "titulo"),
    ("analise", "Aba PROJETINHOS, bloco ANÁLISES", "titulo, descricao, tags, link"),
    ("projeto_curso", "Aba PROJETINHOS, bloco PROJETOS DE CURSOS", "titulo, descricao, tags, link"),
    ("certificado", "Aba CERTIFICADOS, bloco CERTIFICADOS",
     "titulo, detalhe (instituição · ano · horas), tags, link ou arquivo, miniatura"),
    ("em_andamento", "Aba CERTIFICADOS, bloco EM ANDAMENTO", "titulo, detalhe, tags"),
    ("intro_sugestoes", "Aba SUGESTÃO DE CURSOS, texto de abertura", "descricao"),
    ("sugestao", "Aba SUGESTÃO DE CURSOS, cards de indicação",
     "titulo, detalhe (plataforma · nível), descricao (motivo), tags, link"),
    ("contato", "Caixa Contatos (botões)", "titulo = rótulo do botão; link"),
]

EXEMPLOS = [
    {"tipo": "certificado", "titulo": "EXEMPLO: Nome do certificado", "detalhe": "Instituição · 2025 · 20h",
     "tags": "Tema; Outro tema", "arquivo": "exemplo.pdf", "mostrar": "não"},
    {"tipo": "em_andamento", "titulo": "EXEMPLO: Nome do curso em andamento",
     "detalhe": "Plataforma · previsão: mês/ano", "tags": "Tema", "mostrar": "não"},
    {"tipo": "sugestao", "titulo": "EXEMPLO: Nome do curso", "detalhe": "Plataforma · Iniciante",
     "descricao": "Por que eu recomendo este curso, em uma ou duas frases.", "tags": "Tema",
     "link": "https://exemplo.com", "mostrar": "não"},
]

ROSA = PatternFill("solid", start_color="FF9ECF", end_color="FF9ECF")
ROSA_CLARO = PatternFill("solid", start_color="FFDAEC", end_color="FFDAEC")
NEGRITO = Font(bold=True, color="2A1244")
QUEBRA = Alignment(wrap_text=True, vertical="top")


def ler_padrao():
    html = INDEX.read_text(encoding="utf-8")
    bloco = re.search(r"const PADRAO = \[(.*?)\n\];", html, re.S)
    if not bloco:
        raise SystemExit("Não encontrei o array PADRAO no index.html")
    linhas = []
    for obj in re.findall(r"\{(.*?)\}\s*,?\s*$", bloco.group(1), re.M):
        pares = re.findall(r'(\w+):\s*("(?:[^"\\]|\\.)*")', obj)
        linhas.append({k: json.loads(v) for k, v in pares})
    return linhas


def aba_dados(wb, linhas):
    ws = wb.active
    ws.title = "Dados"
    ws.append(COLUNAS)
    for celula in ws[1]:
        celula.fill = ROSA
        celula.font = NEGRITO
        celula.alignment = QUEBRA
    for linha in linhas:
        ws.append([linha.get(c, "") for c in COLUNAS])
    for i, coluna in enumerate(COLUNAS, start=1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = LARGURAS[coluna]
    for linha in ws.iter_rows(min_row=2):
        for celula in linha:
            celula.alignment = QUEBRA
    ws.freeze_panes = "A2"

    ultima = 1000
    dv_tipo = DataValidation(type="list", formula1='"' + ",".join(t for t, _, _ in TIPOS) + '"', allow_blank=True)
    dv_tipo.error = "Escolha um tipo da lista."
    dv_tipo.errorTitle = "Tipo inválido"
    dv_mostrar = DataValidation(type="list", formula1='"sim,não"', allow_blank=True)
    ws.add_data_validation(dv_tipo)
    ws.add_data_validation(dv_mostrar)
    dv_tipo.add(f"A2:A{ultima}")
    dv_mostrar.add(f"I2:I{ultima}")


def aba_como_usar(wb):
    ws = wb.create_sheet("Como usar")
    instrucoes = [
        "COMO USAR ESTA PLANILHA",
        "1. Cada linha da aba Dados é um item do site. A ordem das linhas é a ordem na tela.",
        "2. Escolha o tipo na lista suspensa da coluna tipo (veja a tabela abaixo).",
        "3. Para esconder uma linha sem apagá-la, escolha não na coluna mostrar.",
        "4. Em tags, separe as etiquetas com ponto e vírgula. Exemplo: Excel; BI",
        "5. Em arquivo e miniatura, escreva só o nome do arquivo que está na pasta certificados/ (ex.: excel.pdf).",
        "6. Se o certificado tiver um link (ex.: página de validação), use a coluna link: ela tem prioridade sobre arquivo.",
        "7. Não renomeie os títulos da primeira linha da aba Dados.",
        "",
    ]
    for texto in instrucoes:
        ws.append([texto])
    ws["A1"].font = Font(bold=True, size=14, color="5E2A8A")

    ws.append(["tipo", "onde aparece", "colunas que usa"])
    cab = ws.max_row
    for celula in ws[cab]:
        celula.fill = ROSA
        celula.font = NEGRITO
    for i, linha in enumerate(TIPOS):
        ws.append(list(linha))
        if i % 2:
            for celula in ws[ws.max_row]:
                celula.fill = ROSA_CLARO
    for linha in ws.iter_rows(min_row=cab):
        for celula in linha:
            celula.alignment = QUEBRA
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 50
    ws.column_dimensions["C"].width = 60


def main():
    linhas = ler_padrao()
    for exemplo in EXEMPLOS:
        ja_existe = any(l.get("tipo") == exemplo["tipo"] and l.get("titulo", "").startswith("EXEMPLO")
                        for l in linhas)
        if not ja_existe:
            linhas.append(exemplo)
    wb = Workbook()
    aba_dados(wb, linhas)
    aba_como_usar(wb)
    wb.save(SAIDA)
    print(f"{SAIDA.name}: {len(linhas)} linhas de dados")


if __name__ == "__main__":
    main()
