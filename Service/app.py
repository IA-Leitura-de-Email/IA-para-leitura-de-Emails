from flask import Flask, request, jsonify
from flask_cors import CORS
import google.genai as genai

from config.settings import API_KEY
from Service.email_service import EmailService

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=API_KEY)
service = EmailService(client)


@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados = request.json

    if not dados or not dados.get('email'):
        return jsonify({"erro": "Email obrigatório"}), 400

    try:
        resposta = service.processar_email(dados['email'])

        return jsonify({
            "resposta": resposta
        })

    except Exception as e:
        return jsonify({
            "erro": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)