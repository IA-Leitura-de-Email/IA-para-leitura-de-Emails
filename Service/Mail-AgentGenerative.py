import os
import PyPDF2
import google.generativeai as genai
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
genai.configure(api_key=API_KEY)

# Modelo Gemini utilizado
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

# ==============================
# DEFINIÇÃO DO CAMINHO DA BASE DE CONHECIMENTO
# ==============================
# O sistema localiza automaticamente a pasta base_conhecimento
# independente do computador onde o projeto estiver rodando.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DOCUMENTOS = os.path.join(BASE_DIR, "Knowledge_base", "base_conhecimento")

# Verificação de existência da pasta
if not os.path.exists(PASTA_DOCUMENTOS):
    print(f"Pasta não encontrada: {PASTA_DOCUMENTOS}")

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
        print(f"Erro ao ler PDF {caminho_pdf}: {e}")

    return texto

# ==============================
# FUNÇÃO: BUSCA DE DOCUMENTOS RELEVANTES
# ==============================
# Filtra os PDFs da base de conhecimento e retorna apenas
# os documentos que possuem palavras relacionadas ao email recebido.

def buscar_documentos_relevantes(email, pasta):
    base = ""

    # Palavras irrelevantes removidas da busca
    stopwords = ["de", "a", "o", "para", "com", "do", "da", "e", "em"]

    # Divide o email em palavras úteis
    palavras_email = [
        palavra for palavra in email.lower().split()
        if palavra not in stopwords
    ]

    # Se a pasta não existir, retorna vazio
    if not os.path.exists(pasta):
        return ""

    # Percorre todos os arquivos PDF da pasta
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):

            caminho_pdf = os.path.join(pasta, arquivo)

            # Lê o conteúdo do PDF
            texto = ler_pdf(caminho_pdf)

            # Verifica se alguma palavra do email aparece no PDF
            if any(palavra in texto.lower() for palavra in palavras_email):

                base += f"\nDOCUMENTO: {arquivo}\n"

                # Limita tamanho do texto enviado à IA
                base += texto[:3000]

                base += "\n"

    # Exibe no terminal os documentos encontrados
    print("Documentos encontrados:")
    print(base)

    return base

# ==============================
# ROTA PRINCIPAL DA API
# ==============================
# Recebe um email do frontend, busca documentos relevantes
# e envia contexto filtrado para a IA.

@app.route('/perguntar', methods=['POST'])
def perguntar():

    # Captura JSON enviado pelo frontend
    dados = request.json

    # Extrai conteúdo do email
    email_cliente = dados.get('email', '')

    # Busca apenas documentos relacionados ao email
    base_filtrada = buscar_documentos_relevantes(email_cliente, PASTA_DOCUMENTOS)

    # Caso nenhum documento seja encontrado
    if not base_filtrada:
        return jsonify({
            "resposta": "Não encontrei informações relevantes na base de conhecimento."
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
    try:
        resposta = model.generate_content(prompt)

        return jsonify({
            "resposta": resposta.text
        })

    except Exception as e:
        return jsonify({
            "erro": str(e)
        }), 500

# ==============================
# EXECUÇÃO DO SERVIDOR
# ==============================
# Inicia a API localmente na porta 5000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)