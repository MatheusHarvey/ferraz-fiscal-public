import requests
import pandas as pd
from pathlib import Path
from loguru import logger
from config import BASE_URL, CODIGO_IBGE, ANOS

# Pastas de saída
RAW_DIR = Path("data/raw/siconfi")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def buscar_rreo(ano: int, periodo: int) -> pd.DataFrame | None:
    """
    Busca o Relatório Resumido de Execução Orçamentária (RREO).
    Período = bimestre (1 a 6).
    """
    url = f"{BASE_URL}/rreo"
    params = {
        "an_exercicio": ano,
        "nr_periodo": periodo,
        "co_tipo_demonstrativo": "RREO",
        "no_municipio": "Ferraz de Vasconcelos",
        "co_municipio": CODIGO_IBGE,
    }

    logger.info(f"Buscando RREO {ano} — bimestre {periodo}...")

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        dados = response.json()

        if not dados.get("items"):
            logger.warning(f"Sem dados para RREO {ano} bimestre {periodo}")
            return None

        df = pd.DataFrame(dados["items"])
        logger.success(f"RREO {ano} bimestre {periodo} — {len(df)} registros")
        return df

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {e}")
        return None


def salvar(df: pd.DataFrame, nome: str):
    caminho = RAW_DIR / f"{nome}.csv"
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    logger.success(f"Salvo em {caminho}")


if __name__ == "__main__":
    todos = []

    for ano in ANOS:
        for bimestre in range(1, 7):
            df = buscar_rreo(ano, bimestre)
            if df is not None:
                todos.append(df)

    if todos:
        resultado = pd.concat(todos, ignore_index=True)
        salvar(resultado, "rreo_ferraz")
        print(f"\nTotal de registros coletados: {len(resultado)}")
    else:
        print("Nenhum dado coletado. Verifique os logs acima.")