import os
import re
import PyPDF2
# [CORREÇÃO 7] Migração para o novo pacote google.genai.
# O pacote google.generativeai foi descontinuado pelo Google e não receberá
# mais atualizações. A nova biblioteca é google.genai.
# Para instalar: pip install google-genai
import google.genai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ==============================
# INICIALIZAÇÃO DA API FLASK
# ==============================
# Flask será responsável por receber requisições HTTP
# e retornar respostas da IA para o frontend.

app = Flask(__name__)
CORS(app)  # Permite comunicação entre frontend e backend

# ==============================
# CONFIGURAÇÕES DA IA
# ==============================
# Carrega variáveis do arquivo .env (API_KEY)

load_dotenv()

API_KEY = os.getenv("API_KEY")

# [CORREÇÃO 1] Valida se a API_KEY foi carregada antes de tentar configurar o Gemini.
# Evita um erro genérico difícil de debugar caso o .env esteja ausente ou incorreto.
if not API_KEY:
    raise ValueError("API_KEY não encontrada. Verifique o arquivo .env.")

# [CORREÇÃO 7 - continuação] Nova forma de inicializar o cliente com google.genai
client = genai.Client(api_key=API_KEY)

# Modelo Gemini utilizado
MODELO = "gemini-2.0-flash"

# ==============================
# DEFINIÇÃO DO CAMINHO DA BASE DE CONHECIMENTO
# ==============================
# O sistema localiza automaticamente a pasta base_conhecimento
# independente do computador onde o projeto estiver rodando.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DOCUMENTOS = os.path.join(BASE_DIR, "Knowledge_base", "base_conhecimento")

# Verificação de existência da pasta
if not os.path.exists(PASTA_DOCUMENTOS):
    print(f"[AVISO] Pasta não encontrada: {PASTA_DOCUMENTOS}")

# ==============================
# STOPWORDS EM PORTUGUÊS
# ==============================
# [CORREÇÃO 2] Lista ampliada de palavras irrelevantes para a busca.
# A lista original era muito curta e permitia falsos positivos com palavras
# comuns como "não", "que", "por", "um", etc.

STOPWORDS = {
    # Artigos e preposições
    "de", "a", "o", "para", "com", "do", "da", "e", "em",
    "um", "uma", "os", "as", "no", "na", "nos", "nas",
    "ao", "aos", "às", "pelo", "pela", "pelos", "pelas",
    # Conjunções e pronomes
    "que", "não", "se", "por", "mais", "mas", "ou", "ele",
    "ela", "eles", "elas", "meu", "minha", "seu", "sua",
    "isso", "este", "esta", "esse", "essa", "isto",
    # Verbos comuns
    "foi", "ser", "ter", "tem", "há", "já", "também",
    "como", "quando", "onde", "qual", "quais",
    # [CORREÇÃO 8] Termos técnicos genéricos que aparecem em TODOS os datasheets
    # e causavam falsos positivos — quase todo PDF contém "especificações",
    # "manual", "produto", etc., tornando a filtragem ineficaz.
    "especificações", "especificacoes", "especificacao", "especificação",
    "manual", "guia", "datasheet", "produto", "modelo", "sobre",
    "preciso", "gostaria", "saber", "informações", "informacoes",
    "técnicas", "tecnicas", "favor", "ajuda", "ola", "olá",
    "bom", "dia", "boa", "tarde", "noite", "prezado", "prezados",
}

# ==============================
# LIMITE DE CARACTERES POR DOCUMENTO
# ==============================
# [CORREÇÃO 3] Constante extraída para facilitar ajuste futuro.
# Em vez de cortar sempre nos primeiros 3000 chars (que podem ser cabeçalhos
# irrelevantes), agora extraímos trechos ao redor das palavras encontradas,
# preservando contexto útil. Este valor define o tamanho de cada trecho.

TAMANHO_TRECHO = 500  # caracteres ao redor de cada ocorrência
MAX_TRECHOS_POR_DOC = 5  # máximo de trechos extraídos por documento

# ==============================
# FUNÇÃO: LEITURA DE PDF
# ==============================
# Responsável por abrir um arquivo PDF e extrair todo o texto.

def ler_pdf(caminho_pdf):
    texto = ""

    try:
        with open(caminho_pdf, "rb") as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)

            for pagina in leitor.pages:
                conteudo = pagina.extract_text()

                if conteudo:
                    texto += conteudo + "\n"

    except Exception as e:
        print(f"[ERRO] Falha ao ler PDF '{caminho_pdf}': {e}")

    return texto

# ==============================
# FUNÇÃO: EXTRAÇÃO DE TRECHOS RELEVANTES
# ==============================
# [CORREÇÃO 3 - continuação] Em vez de truncar o documento nos primeiros N chars,
# localiza as ocorrências das palavras-chave no texto e extrai janelas de contexto
# ao redor de cada uma. Isso garante que a IA receba trechos realmente úteis,
# mesmo que a informação relevante esteja no meio ou no fim do PDF.

def extrair_trechos(texto, palavras, tamanho=TAMANHO_TRECHO, max_trechos=MAX_TRECHOS_POR_DOC):
    texto_lower = texto.lower()
    regioes = []

    for palavra in palavras:
        # [CORREÇÃO 4] Usa \b para matching de palavra inteira (word boundary).
        # Evita que "sa" dê match em "casa", "usar", "passar", etc.
        for match in re.finditer(r'\b' + re.escape(palavra) + r'\b', texto_lower):
            inicio = max(0, match.start() - tamanho)
            fim = min(len(texto), match.end() + tamanho)
            regioes.append((inicio, fim))

    if not regioes:
        return ""

    # Mescla regiões sobrepostas para evitar repetição de trechos
    regioes.sort()
    regioes_mescladas = [regioes[0]]

    for inicio, fim in regioes[1:]:
        ultimo_inicio, ultimo_fim = regioes_mescladas[-1]
        if inicio <= ultimo_fim:
            regioes_mescladas[-1] = (ultimo_inicio, max(ultimo_fim, fim))
        else:
            regioes_mescladas.append((inicio, fim))

    # Limita ao número máximo de trechos por documento
    trechos = [
        f"[...] {texto[i:f].strip()} [...]"
        for i, f in regioes_mescladas[:max_trechos]
    ]

    return "\n".join(trechos)

# ==============================
# FUNÇÃO: BUSCA DE DOCUMENTOS RELEVANTES
# ==============================
# Filtra os PDFs da base de conhecimento e retorna apenas
# os documentos que possuem palavras relacionadas ao email recebido.

def buscar_documentos_relevantes(email, pasta):
    base = ""

    # Divide o email em palavras úteis, removendo stopwords e pontuação
    palavras_email = [
        re.sub(r'[^\w]', '', palavra)          # remove pontuação
        for palavra in email.lower().split()
        if palavra not in STOPWORDS and len(palavra) > 2  # ignora palavras muito curtas
    ]

    # Remove palavras vazias que sobraram após limpeza
    palavras_email = [p for p in palavras_email if p]

    # Se não restar nenhuma palavra útil, retorna vazio
    if not palavras_email:
        return ""

    # Se a pasta não existir, retorna vazio
    if not os.path.exists(pasta):
        return ""

    documentos_encontrados = []

    # Percorre todos os arquivos PDF da pasta
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):

            caminho_pdf = os.path.join(pasta, arquivo)

            # Lê o conteúdo do PDF
            texto = ler_pdf(caminho_pdf)

            if not texto:
                continue

            # [CORREÇÃO 4 + 8] Sistema de pontuação por relevância.
            # Em vez de incluir o documento se QUALQUER palavra der match (any),
            # contamos quantas palavras distintas do email aparecem no PDF.
            # O documento só é incluído se atingir um mínimo de matches.
            # Isso resolve o caso "especificações do rw 6302": após remover
            # stopwords e termos genéricos, só restam "rw" e "6302" —
            # e apenas os PDFs que contêm ambos serão incluídos.
            texto_lower = texto.lower()
            palavras_encontradas = sum(
                1 for palavra in palavras_email
                if re.search(r'\b' + re.escape(palavra) + r'\b', texto_lower)
            )

            # Threshold: pelo menos 50% das palavras-chave devem dar match,
            # com mínimo absoluto de 1 para emails com poucas palavras.
            total_palavras = len(palavras_email)
            threshold = max(1, round(total_palavras * 0.5))
            tem_match = palavras_encontradas >= threshold

            if tem_match:
                # [CORREÇÃO 3] Extrai só os trechos relevantes ao invés de
                # truncar nos primeiros 3000 chars indiscriminadamente.
                trechos = extrair_trechos(texto, palavras_email)

                if trechos:
                    base += f"\nDOCUMENTO: {arquivo}\n"
                    base += trechos
                    base += "\n"
                    documentos_encontrados.append(arquivo)

    # [CORREÇÃO 5] Log enxuto com palavras-chave utilizadas na busca.
    print(f"[INFO] Palavras-chave utilizadas: {palavras_email}")
    if documentos_encontrados:
        print(f"[INFO] {len(documentos_encontrados)} documento(s) encontrado(s): {documentos_encontrados}")
    else:
        print("[INFO] Nenhum documento relevante encontrado para este email.")

    return base

# ==============================
# ROTA PRINCIPAL DA API
# ==============================
# Recebe um email do frontend, busca documentos relevantes
# e envia contexto filtrado para a IA.

@app.route('/perguntar', methods=['POST'])
def perguntar():

    # [CORREÇÃO 6] Valida se o body da requisição é um JSON válido.
    # request.json retorna None se o Content-Type não for application/json
    # ou se o corpo estiver malformado, causando AttributeError na linha seguinte.
    dados = request.json

    if not dados:
        return jsonify({
            "erro": "Requisição inválida. Envie um JSON com o campo 'email'."
        }), 400

    # Extrai conteúdo do email
    email_cliente = dados.get('email', '').strip()

    # [CORREÇÃO 6 - continuação] Valida se o campo 'email' foi enviado e não está vazio.
    if not email_cliente:
        return jsonify({
            "erro": "O campo 'email' é obrigatório e não pode estar vazio."
        }), 400

    # Busca apenas documentos relacionados ao email
    base_filtrada = buscar_documentos_relevantes(email_cliente, PASTA_DOCUMENTOS)

    # Caso nenhum documento seja encontrado
    if not base_filtrada:
        return jsonify({
            "resposta": "Não encontrei informações relevantes na base de conhecimento para este email."
        })

    # ==============================
    # PROMPT ENVIADO AO GEMINI
    # ==============================
    prompt = f"""
Você é um atendente de suporte da INTELBRAS.
Use SOMENTE os trechos abaixo.
Não invente informações.
Se não encontrar resposta, diga que não possui a informação.

BASE DE CONHECIMENTO:
{base_filtrada}

EMAIL DO CLIENTE:
{email_cliente}

REGRAS:
- FORMATO DE DOCUMENTAÇÃO
- RESPOSTA BREVE
- PROFISSIONAL
- FOQUE SOMENTE NO PEDIDO DO CLIENTE
"""

    # ==============================
    # CHAMADA AO MODELO GEMINI
    # ==============================
    # [CORREÇÃO 7] Atualizado para a nova API google.genai
    try:
        resposta = client.models.generate_content(
            model=MODELO,
            contents=prompt
        )

        return jsonify({
            "resposta": resposta.text
        })

    except Exception as e:
        print(f"[ERRO] Falha ao chamar o Gemini: {e}")
        return jsonify({
            "erro": str(e)
        }), 500

# ==============================
# EXECUÇÃO DO SERVIDOR
# ==============================
# Inicia a API localmente na porta 5000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)