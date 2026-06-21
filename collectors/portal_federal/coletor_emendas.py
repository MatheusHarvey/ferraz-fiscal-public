import requests
import pandas as pd
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
import os
import time

load_dotenv(Path("../../.env"))

CHAVE = os.getenv("PORTAL_TRANSPARENCIA_KEY")
CODIGO_IBGE = "3515707"
RAW_DIR = Path("../../data/raw/portal_federal")
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "Accept": "application/json",
    "chave-api-dados": CHAVE,
}

def buscar_pagina(pagina: int) -> list:
    r = requests.get(
        "https://api.portaldatransparencia.gov.br/api-de-dados/emendas",
        params={
            "codigoIbge": CODIGO_IBGE,
            "pagina": pagina,
        },
        headers=HEADERS,
        timeout=30,
    )
    if r.status_code == 200:
        return r.json()
    else:
        logger.error(f"Erro página {pagina}: {r.status_code} — {r.text[:200]}")
        return []

def main():
    logger.info("Iniciando coleta de emendas parlamentares de Ferraz de Vasconcelos...")
    todos = []
    pagina = 1

    while True:
        logger.info(f"Buscando página {pagina}...")
        dados = buscar_pagina(pagina)

        if not dados:
            logger.info("Sem mais dados — coleta concluída.")
            break

        todos.extend(dados)
        logger.success(f"Página {pagina} — {len(dados)} registros")

        if len(dados) < 500:
            break

        pagina += 1
        time.sleep(0.5)

    if todos:
        df = pd.json_normalize(todos)
        saida = RAW_DIR / "emendas_ferraz.csv"
        df.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
        logger.success(f"Total: {len(df)} emendas salvas em {saida}")

        print(f"\nTotal de emendas: {len(df)}")

        if "situacao" in df.columns:
            print("\nPor situação:")
            print(df["situacao"].value_counts().to_string())

        for col in ["valorEmpenhado", "valorPago"]:
            if col in df.columns:
                total = pd.to_numeric(df[col], errors="coerce").sum()
                print(f"\n{col}: R$ {total:,.2f}")
    else:
        logger.warning("Nenhum dado coletado.")

if __name__ == "__main__":
    main()