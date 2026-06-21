import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import json

load_dotenv(Path("../../.env"))
chave = os.getenv("PORTAL_TRANSPARENCIA_KEY")

headers = {
    "Accept": "application/json",
    "chave-api-dados": chave,
}

r = requests.get(
    "https://api.portaldatransparencia.gov.br/api-de-dados/convenios",
    params={
        "codigoIBGE": "3515707",
        "pagina": 1,
    },
    headers=headers,
    timeout=30,
)

print(f"Status: {r.status_code}")
if r.status_code == 200:
    dados = r.json()
    print(f"Registros: {len(dados)}")
    if dados:
        print(json.dumps(dados[0], indent=2, ensure_ascii=False))
else:
    print(r.text)