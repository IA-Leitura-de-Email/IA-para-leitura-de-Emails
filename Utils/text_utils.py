import re
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

def limpar_palavras(email):
    palavras = [
        re.sub(r'[^\w]', '', p)
        for p in email.lower().split()
        if p not in STOPWORDS and len(p) > 2
    ]
    return [p for p in palavras if p]

# ==============================
# LIMITE DE CARACTERES POR DOCUMENTO
# ==============================
# [CORREÇÃO 3] Constante extraída para facilitar ajuste futuro.
# Em vez de cortar sempre nos primeiros 3000 chars (que podem ser cabeçalhos
# irrelevantes), agora extraímos trechos ao redor das palavras encontradas,
# preservando contexto útil. Este valor define o tamanho de cada trecho.

TAMANHO_TRECHO = 500  # caracteres ao redor de cada ocorrência
MAX_TRECHOS_POR_DOC = 5  # máximo de trechos extraídos por documento
