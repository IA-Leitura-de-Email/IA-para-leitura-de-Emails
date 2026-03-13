import os
import PyPDF2
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Permite que seu HTML/JS acesse esta API

# ==============================
# CONFIGURAÇÕES
# ==============================
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY") # Chave do Google AI Studio
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

PASTA_DOCUMENTOS = os.path.join(os.path.expanduser("~"), "Documents", "../Knowledge_base/base_conhecimento")

# ==============================
# FUNÇÕES DE APOIO
# ==============================
def ler_pdf(caminho_pdf):
    texto = ""
    try:
        with open(caminho_pdf, "rb") as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for pagina in leitor.pages:
                conteudo = pagina.extract_text()
                if conteudo: texto += conteudo + "\n"
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
    return texto

def carregar_documentos(pasta):
    base = ""
    if not os.path.exists(pasta):
        return ""
    for arquivo in os.listdir(pasta): 
        if arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(pasta, arquivo) 
            base += f"\nDOCUMENTO: {arquivo}\n" 
            base += ler_pdf(caminho_pdf) 
            base += "\n"
    return base


# Carrega a base UMA VEZ ao iniciar o servidor
BASE_CONHECIMENTO = carregar_documentos(PASTA_DOCUMENTOS)

# ==============================
# ROTA DA API
# ==============================
@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados = request.json
    email_cliente = dados.get('email', '')

    if not BASE_CONHECIMENTO:
        return jsonify({"erro": "Base de conhecimento vazia ou não encontrada."}), 500

    prompt = f"""
    Você é um atendente de suporte da INTELBRAS.
    Use APENAS as informações da base de conhecimento para responder.
    Se a resposta não estiver nos documentos, diga que o atendimento humano irá verificar.

    BASE DE CONHECIMENTO:
    {BASE_CONHECIMENTO}

    EMAIL DO CLIENTE:
    {email_cliente}

    REGRAS:
    - SEMPRE DEIXE O TEXTO EM FORMATO DE DOCUMENTAÇÃO!
    - FOQUE APENAS NO MENCIONADO PELO CLIENTE!
    - SEJA BREVE E PROFISSIONAL!
    """

    try:
        resposta = model.generate_content(prompt)
        return jsonify({"resposta": resposta.text})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    # Roda o servidor na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
