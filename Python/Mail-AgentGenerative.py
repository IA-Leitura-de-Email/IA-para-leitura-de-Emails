import os
import PyPDF2
import google.generativeai as genai # 

# ==============================
# CONFIGURAÇÕES
# ==============================

API_KEY = "AIzaSyBrtPNH8MVRRsidZ6pEqBtY0l9JkzA3m2E" # Chave do Google AI Studio 

# Configurando a chave na biblioteca do Gemini
genai.configure(api_key=API_KEY)

# Modelo - Generativo
model = genai.GenerativeModel('gemini-flash-lite-latest')

# Caminho ao diretorio, para a fonte de dados.
PASTA_DOCUMENTOS = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "base_conhecimento"
)

# ==============================
# FUNÇÃO PARA LER UM PDF
# ==============================

def ler_pdf(caminho_pdf):
    texto = ""
    with open(caminho_pdf, "rb") as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        for pagina in leitor.pages:
            conteudo = pagina.extract_text()
            if conteudo:
                texto += conteudo + "\n"
    return texto

# ==============================
# FUNÇÃO PARA LER TODOS OS PDFs
# ==============================

def carregar_documentos(pasta):
    base_conhecimento = ""
    print("\nCarregando documentos da empresa...\n")
    
    # Verifica se a pasta existe para evitar erros
    if not os.path.exists(pasta):
        print(f"ERRO: A pasta {pasta} não foi encontrada. Crie a pasta e coloque seus PDFs nela.")
        return ""

    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(pasta, arquivo)
            print(f"Lendo arquivo: {arquivo}")
            texto_pdf = ler_pdf(caminho_pdf)
            base_conhecimento += f"\nDOCUMENTO: {arquivo}\n"
            base_conhecimento += texto_pdf
            base_conhecimento += "\n\n"

    return base_conhecimento

# ==============================
# CARREGAR BASE DE CONHECIMENTO
# ==============================

base_conhecimento = carregar_documentos(PASTA_DOCUMENTOS)

if not base_conhecimento:
    print("Nenhum texto foi carregado. Encerrando o programa.")
    exit()

# ==============================
# ENTRADA DO EMAIL DO CLIENTE
# ==============================

print("\n==============================")
print(" SISTEMA DE RESPOSTA DE EMAIL ")
print("==============================\n")

email_cliente = input("Cole o email do cliente abaixo e pressione ENTER:\n\n")

# ==============================
# PROMPT ENVIADO PARA A IA
# ==============================

prompt = f"""
Você é um atendente de suporte da INTELBRAS.

Use APENAS as informações da base de conhecimento
para responder o cliente.

Se a resposta não estiver nos documentos,
diga que o atendimento humano irá verificar.


BASE DE CONHECIMENTO DA EMPRESA:

{base_conhecimento}

EMAIL DO CLIENTE:

{email_cliente}

SEMPRE DEIXE O TEXTO EM FORMATO DE DOCUMENTAÇÃO!
SEMPRE SEJA BREVE!
NÃO SE ESTENDER NA EXPLICAÇÃO!
Responda o email de forma educada e profissional.
"""

# ==============================
# CHAMADA DA IA (GEMINI)
# ==============================

print("\nGerando resposta... Aguarde.\n")

try:
    # A chamada para o Gemini acontece aqui
    resposta = model.generate_content(prompt)
    texto_resposta = resposta.text
except Exception as e:
    texto_resposta = f"Ocorreu um erro ao chamar a API do Gemini: {e}"

# ==============================
# EXIBIR RESPOSTA
# ==============================

print("==============================")
print(" RESPOSTA GERADA PELA IA ")
print("==============================\n")

print(texto_resposta)
