#import os
from dotenv import load_dotenv 

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