import pandas as pd
from pathlib import Path
from loguru import logger

PROCESSED_DIR = Path("../../data/processed/tce_sp")

def corrigir_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Corrige nomes de colunas com encoding corrompido."""
    novas_colunas = []
    for col in df.columns:
        try:
            nova = col.encode("latin-1").decode("utf-8")
        except:
            nova = col
        novas_colunas.append(nova)
    df.columns = novas_colunas
    return df

def processar(nome_arquivo: str):
    caminho = PROCESSED_DIR / nome_arquivo
    if not caminho.exists():
        logger.warning(f"Arquivo não encontrado: {nome_arquivo}")
        return

    logger.info(f"Corrigindo {nome_arquivo}...")
    df = pd.read_csv(caminho, sep=";", dtype=str, encoding="utf-8-sig")
    df = corrigir_colunas(df)
    df.to_csv(caminho, index=False, encoding="utf-8-sig", sep=";")
    logger.success(f"{nome_arquivo} corrigido — colunas: {df.columns.tolist()[:5]}")

def main():
    processar("licitacoes_ferraz.csv")
    processar("ajustes_ferraz.csv")

if __name__ == "__main__":
    main()