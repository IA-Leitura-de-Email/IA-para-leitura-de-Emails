# 📧 IA para Leitura de Emails

Projeto desenvolvido para **ler e interpretar o conteúdo de e-mails utilizando Inteligência Artificial**.

O sistema processa mensagens (incluindo conteúdo extraído de arquivos PDF) e envia o texto para uma IA generativa que analisa e retorna informações relevantes sobre o conteúdo.

A aplicação utiliza a API do **Google Gemini** através da biblioteca Python **google-generativeai**.

---

# 🎯 Objetivo do Projeto

Automatizar a leitura e interpretação de e-mails para:

* identificar informações importantes
* interpretar o conteúdo da mensagem
* auxiliar na classificação ou tomada de decisão
* reduzir o tempo de leitura manual de e-mails

---

# ⚙️ Tecnologias Utilizadas

* Python
* PyPDF2
* Flask
* Google Generative AI (Gemini)
* API Key
* JSON

Bibliotecas principais:

```
PyPDF2
google-generativeai
```

---

# 📂 Funcionamento do Sistema

Atualmente o sistema realiza as seguintes etapas:

### 1️⃣ Leitura do arquivo

O sistema recebe um **arquivo PDF contendo o conteúdo de um e-mail ou documento**.

---

### 2️⃣ Extração do texto

Utilizando a biblioteca **PyPDF2**, o sistema:

* abre o PDF
* percorre as páginas
* extrai o texto do documento

---

### 3️⃣ Envio para IA

O texto extraído é enviado para o modelo de IA **Google Gemini**, que analisa o conteúdo.

---

### 4️⃣ Interpretação do conteúdo

A IA lê o texto e retorna uma análise baseada no prompt definido no código.

Dependendo da implementação atual, ela pode:

* resumir o e-mail
* interpretar a intenção
* destacar informações importantes

---

# 🧠 Arquitetura Simplificada

```
PDF / Email
     │
     ▼
Extração de texto (PyPDF2)
     │
     ▼
Envio para IA (Google Gemini)
     │
     ▼
Resposta interpretada pela IA
     │
     ▼
Resultado exibido no terminal
```

---

# 🚀 Como Executar o Projeto

## 1️⃣ Clonar o repositório

```
git clone https://github.com/IA-Leitura-de-Email/IA-para-leitura-de-Emails.git
```

---

## 2️⃣ Entrar na pasta do projeto

```
cd IA-para-leitura-de-Emails
```

---

## 3️⃣ Instalar as dependências

Instale as bibliotecas necessárias:

```
pip install PyPDF2
pip install google-generativeai
```

Ou, se preferir:

```
pip install PyPDF2 google-generativeai
```

---

## 4️⃣ Configurar a API Key

Para utilizar o modelo de IA é necessário possuir uma **API Key do Google Gemini**.

No código Python, configure a chave:

```python
import google.generativeai as genai

genai.configure(api_key="SUA_API_KEY_AQUI")
```

---

## 5️⃣ Executar o programa

Execute o arquivo principal do projeto:

```
python main.py
```

*(ou o arquivo Python principal presente no repositório)*

---

# 🧪 Exemplo de Fluxo

Entrada:

```
Arquivo PDF contendo o texto de um e-mail
```

Processo:

```
PDF → Extração de texto → Envio para IA → Análise
```

Saída:

```
Resposta gerada pela IA com interpretação do conteúdo do e-mail
```

