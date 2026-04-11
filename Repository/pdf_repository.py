import os
import re
import PyPDF2
from Utils.text_utils import limpar_palavras

def ler_pdf(caminho):
    texto = ""
    with open(caminho, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            conteudo = page.extract_text()
            if conteudo:
                texto += conteudo + "\n"
    return texto


def extrair_trechos(texto, palavras, tamanho=500):
    texto_lower = texto.lower()
    trechos = []

    for palavra in palavras:
        for match in re.finditer(r'\b' + re.escape(palavra) + r'\b', texto_lower):
            inicio = max(0, match.start() - tamanho)
            fim = min(len(texto), match.end() + tamanho)
            trechos.append(texto[inicio:fim])

    return "\n".join(trechos[:5])


def buscar_documentos(email, pasta):
    palavras = limpar_palavras(email)

    if not palavras or not os.path.exists(pasta):
        return ""

    base = ""

    for arquivo in os.listdir(pasta):
        if not arquivo.endswith(".pdf"):
            continue

        caminho = os.path.join(pasta, arquivo)
        texto = ler_pdf(caminho)

        if not texto:
            continue

        texto_lower = texto.lower()

        matches = sum(
            1 for p in palavras
            if re.search(r'\b' + re.escape(p) + r'\b', texto_lower)
        )

        if matches >= max(1, len(palavras) * 0.5):
            trechos = extrair_trechos(texto, palavras)

            if trechos:
                base += f"\nDOC: {arquivo}\n{trechos}\n"

    return base