import pandas as pd
from pathlib import Path
from loguru import logger

ERRO_DIR = Path("../../data/raw/tce_sp/conjunto-dados/licitacoes-contratos/licitacoes-erro")
PROCESSED_DIR = Path("../../data/processed/tce_sp")

MUNICIPIO = "Ferraz de Vasconcelos"

def ler_csv(arquivo: Path) -> pd.DataFrame | None:
    # Para o arquivo problemático de 2023-09, usa on_bad_lines='skip'
    try:
        df = pd.read_csv(
            arquivo,
            sep=";",
            dtype=str,
            quotechar='"',
            encoding="latin-1",
            on_bad_lines="skip",
        )
        return df
    except Exception as e:
        logger.error(f"Erro ao ler {arquivo.name}: {e}")
        return None

def filtrar_ferraz(df: pd.DataFrame) -> pd.DataFrame:
    col_municipio = next(
        (c for c in df.columns if "unic" in c.lower()),
        None
    )
    if not col_municipio:
        logger.warning("Coluna de município não encontrada")
        return pd.DataFrame()
    return df[df[col_municipio].str.strip() == MUNICIPIO].copy()

def main():
    csvs = sorted(ERRO_DIR.glob("*.csv"))
    logger.info(f"Arquivos encontrados: {len(csvs)}")

    todos = []
    for csv_path in csvs:
        logger.info(f"Processando {csv_path.name}...")
        df = ler_csv(csv_path)

        if df is None or df.empty:
            continue

        ferraz = filtrar_ferraz(df)
        if ferraz.empty:
            logger.warning(f"Ferraz não encontrada em {csv_path.name}")
            continue

        ferraz["arquivo_origem"] = csv_path.name
        logger.success(f"{csv_path.name} — {len(ferraz)} registros")
        todos.append(ferraz)

    if todos:
        df_final = pd.concat(todos, ignore_index=True)

        # Carrega licitações já processadas e concatena
        saida = PROCESSED_DIR / "licitacoes_ferraz.csv"
        if saida.exists():
            df_existente = pd.read_csv(saida, sep=";", dtype=str, encoding="utf-8-sig")
            df_final = pd.concat([df_existente, df_final], ignore_index=True)
            logger.info("Concatenado com licitacoes_ferraz.csv existente")

        df_final.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
        logger.success(f"Total final: {len(df_final)} registros em licitacoes_ferraz.csv")
        print(f"\nRegistros adicionados dos arquivos com erro: {len(pd.concat(todos))}")
        print(f"Total geral de licitações: {len(df_final)}")
    else:
        print("Nenhum dado de Ferraz encontrado nos arquivos.")

if __name__ == "__main__":
    main()