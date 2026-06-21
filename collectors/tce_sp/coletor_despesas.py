import requests
import pandas as pd
from pathlib import Path
from loguru import logger
import time

RAW_DIR = Path("../../data/raw/tce_sp")
RAW_DIR.mkdir(parents=True, exist_ok=True)

MUNICIPIO = "ferraz-de-vasconcelos"
BASE_URL = "https://transparencia.tce.sp.gov.br/api/json"

# API cobre 2014-2019
ANOS = [2014, 2015, 2016, 2017, 2018, 2019]
MESES = range(1, 13)

def buscar_despesas(ano: int, mes: int) -> list:
    url = f"{BASE_URL}/despesas/{MUNICIPIO}/{ano}/{mes}"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            dados = r.json()
            return dados if isinstance(dados, list) else []
        else:
            logger.warning(f"Erro {r.status_code} — {ano}/{mes}")
            return []
    except Exception as e:
        logger.error(f"Exceção {ano}/{mes}: {e}")
        return []

def main():
    logger.info(f"Iniciando coleta TCE-SP — {MUNICIPIO}")
    todos = []

    for ano in ANOS:
        registros_ano = []
        for mes in MESES:
            dados = buscar_despesas(ano, mes)
            if dados:
                for d in dados:
                    d["ano"] = ano
                    d["mes_num"] = mes
                registros_ano.extend(dados)
                logger.success(f"{ano}/{mes:02d} — {len(dados)} registros")
            else:
                logger.warning(f"{ano}/{mes:02d} — sem dados")
            time.sleep(0.3)

        if registros_ano:
            df_ano = pd.DataFrame(registros_ano)
            saida = RAW_DIR / f"despesas_{ano}.csv"
            df_ano.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
            logger.success(f"Salvo: despesas_{ano}.csv — {len(df_ano)} registros")
            todos.append(df_ano)

    if todos:
        df_total = pd.concat(todos, ignore_index=True)
        logger.success(f"Total geral: {len(df_total)} registros")
        print(f"\nTotal de registros: {len(df_total)}")
        print(f"\nTop 10 fornecedores:")
        print(df_total.groupby("nm_fornecedor")["vl_despesa"].count()
              .sort_values(ascending=False).head(10).to_string())
    else:
        logger.warning("Nenhum dado coletado.")

if __name__ == "__main__":
    main()