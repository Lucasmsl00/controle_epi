# licenca.py
import json
import requests
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os

CAMINHO_CACHE = "cache.dat"
CAMINHO_CHAVE = "chave.key"
URL_JSON = "http://localhost/licensas.json"  # substitua pelo seu link
TOLERANCIA_DIAS = 5

def gerar_chave_local():
    if not os.path.exists(CAMINHO_CHAVE):
        chave = Fernet.generate_key()
        with open(CAMINHO_CHAVE, "wb") as f:
            f.write(chave)

def carregar_chave_local():
    with open(CAMINHO_CHAVE, "rb") as f:
        return f.read()

def salvar_cache_criptografado(dados):
    chave = carregar_chave_local()
    fernet = Fernet(chave)
    texto = json.dumps(dados).encode()
    criptografado = fernet.encrypt(texto)

    with open(CAMINHO_CACHE, "wb") as f:
        f.write(criptografado)

def carregar_cache_criptografado():
    if not os.path.exists(CAMINHO_CACHE):
        return None

    chave = carregar_chave_local()
    fernet = Fernet(chave)

    try:
        with open(CAMINHO_CACHE, "rb") as f:
            criptografado = f.read()
        texto = fernet.decrypt(criptografado)
        return json.loads(texto)
    except Exception:
        return None

def verificar_online(chave_licenca):
    try:
        resposta = requests.get(URL_JSON, timeout=5)
        licencas = resposta.json()
        dados = licencas.get(chave_licenca)
        if not dados or dados["status"] != "ativo":
            return None

        expira = datetime.strptime(dados["expira_em"], "%Y-%m-%d")
        cache = {
            "expira_em": dados["expira_em"],
            "ultima_verificacao": datetime.now().strftime("%Y-%m-%d")
        }
        salvar_cache_criptografado(cache)
        return expira
    except Exception as e:
        print("Erro ao verificar online:", e)
        return None

def verificar_licenca():
    gerar_chave_local()

    try:
        with open("config.json") as f:
            config = json.load(f)
            chave_licenca = config.get("chave_licenca")
    except Exception:
        return False

    # 1. Tenta verificar online
    expira_em = verificar_online(chave_licenca)
    if expira_em:
        return datetime.now() <= expira_em

    # 2. Se falhar, usa cache local
    cache = carregar_cache_criptografado()
    if not cache:
        return False

    try:
        expira_em = datetime.strptime(cache["expira_em"], "%Y-%m-%d")
        ultima_verif = datetime.strptime(cache["ultima_verificacao"], "%Y-%m-%d")
        dias_desde_ultima = (datetime.now() - ultima_verif).days

        if datetime.now() <= expira_em and dias_desde_ultima <= TOLERANCIA_DIAS:
            return True
    except:
        pass

    return False
