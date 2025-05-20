import requests
import os
from dotenv import load_dotenv

load_dotenv()

def obter_token() -> str:
    url = "https://sso.cloud.pje.jus.br/auth/realms/pje/protocol/openid-connect/token"

    usuario = os.getenv("USUARIO_PDPJ")
    senha = os.getenv("SENHA_PDPJ")

    if not usuario or not senha:
        raise Exception("❌ Variáveis USUARIO_PDPJ ou SENHA_PDPJ não definidas no .env")

    payload = {
        "grant_type": "password",
        "client_id": "jusbr",  # ajuste se necessário
        "username": usuario,
        "password": senha
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        raise Exception(f"Erro ao obter token: {response.status_code} - {response.text}")
