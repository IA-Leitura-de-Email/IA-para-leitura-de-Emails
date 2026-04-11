from Repository.pdf_repository import buscar_documentos
from config.settings import PASTA_DOCUMENTOS, MODELO
import google.genai as genai


class EmailService:

    def __init__(self, client):
        self.client = client

    def processar_email(self, email):
        base = buscar_documentos(email, PASTA_DOCUMENTOS)

        if not base:
            return "Não encontrei informações relevantes na base de conhecimento."

        prompt = f"""
Você é um atendente de suporte da INTELBRAS.
Use SOMENTE os trechos abaixo.
Não invente informações.
Se não encontrar resposta, diga que não possui a informação na base de conhecimento.

BASE:
{base}

EMAIL:
{email}

REGRAS:
- FORMATO DE DOCUMENTAÇÃO
- RESPOSTA BREVE
- PROFISSIONAL
- FOQUE SOMENTE NO PEDIDO DO CLIENTE
"""
        
        resposta = self.client.models.generate_content(
            model=MODELO,
            contents=prompt
        )

        return resposta.text