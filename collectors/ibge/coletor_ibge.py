import requests
import pandas as pd
from pathlib import Path

CODIGO_IBGE = "3515707"
PROCESSED_DIR = Path("data/processed/ibge")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

BASE_V3 = "https://servicodados.ibge.gov.br/api/v3/agregados"

def buscar(agregado: str, variavel: str, periodos: str = "2010|2020|2021|2022") -> dict:
    url = f"{BASE_V3}/{agregado}/periodos/{periodos}/variaveis/{variavel}"
    params = {"localidades": f"N6[{CODIGO_IBGE}]"}
    r = requests.get(url, params=params, timeout=30)
    if r.status_code == 200:
        return r.json()
    return {}

def extrair_valor(dados: list) -> dict:
    """Extrai valores por período de um resultado da API v3."""
    resultados = {}
    if not dados:
        return resultados
    for item in dados:
        series = item.get("resultados", [])
        for serie in series:
            for localidade in serie.get("series", []):
                for periodo, valor in localidade.get("serie", {}).items():
                    resultados[periodo] = valor
    return resultados

def main():
    print("=" * 60)
    print("IBGE API v3 — FERRAZ DE VASCONCELOS")
    print("=" * 60)

    indicadores = []

    # 1. População — Censo 2022 (agregado 9514, variável 93)
    print("\n[1] Buscando população (Censo 2022)...")
    dados = buscar("9514", "93", "2022")
    pop = extrair_valor(dados)
    print(f"  Resultado: {pop}")
    indicadores.append({"indicador": "populacao_censo", "dados": pop})

    # 2. PIB per capita (agregado 5938, variável 37)
    print("\n[2] Buscando PIB per capita...")
    dados = buscar("5938", "37", "2019|2020|2021")
    pib = extrair_valor(dados)
    print(f"  Resultado: {pib}")
    indicadores.append({"indicador": "pib_per_capita", "dados": pib})

    # 3. IDHM (agregado 5938, variável 30255) — disponível só no Atlas
    # Vamos tentar via endpoint diferente
    print("\n[3] Buscando IDHM...")
    r = requests.get(
        "https://apisidra.ibge.gov.br/values/t/9605/n6/3515707/v/allthemes",
        timeout=15
    )
    print(f"  Status: {r.status_code} — {r.text[:200]}")

    # 4. Renda per capita (agregado 9921, variável 10162)
    print("\n[4] Buscando renda per capita (Censo 2022)...")
    dados = buscar("9921", "10162", "2022")
    renda = extrair_valor(dados)
    print(f"  Resultado: {renda}")
    indicadores.append({"indicador": "renda_per_capita", "dados": renda})

    # 5. Taxa de analfabetismo (agregado 9543, variável 10100)
    print("\n[5] Buscando taxa de analfabetismo (Censo 2022)...")
    dados = buscar("9543", "10100", "2022")
    analf = extrair_valor(dados)
    print(f"  Resultado: {analf}")
    indicadores.append({"indicador": "taxa_analfabetismo", "dados": analf})

    # 6. Esgotamento sanitário (agregado 9533, variável 10148)
    print("\n[6] Buscando acesso a esgotamento sanitário (Censo 2022)...")
    dados = buscar("9533", "10148", "2022")
    esgoto = extrair_valor(dados)
    print(f"  Resultado: {esgoto}")
    indicadores.append({"indicador": "esgotamento_sanitario", "dados": esgoto})

if __name__ == "__main__":
    main()