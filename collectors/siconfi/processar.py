import pandas as pd
from pathlib import Path
from loguru import logger

# Configuração
CODIGO_FERRAZ = 3515707
RAW_DIR = Path("../../data/raw/siconfi")
PROCESSED_DIR = Path("../../data/processed/siconfi")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Mapeamento: nome do arquivo CSV -> nome do output
ARQUIVOS = {
    "receitas.csv": "receitas",
    "despesas.csv": "despesas",
    "despesas_funcao.csv": "despesas_funcao",
}

def ler_finbra(caminho: Path) -> pd.DataFrame:
    return pd.read_csv(
        caminho,
        sep=";",
        skiprows=3,
        encoding="latin-1",
        decimal=",",
    )

def filtrar_ferraz(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Cod.IBGE"] == CODIGO_FERRAZ].copy()

def processar_pasta(ano: int, pasta: Path):
    logger.info(f"Processando ano {ano}...")

    for nome_arquivo, nome_saida in ARQUIVOS.items():
        arquivo = pasta / nome_arquivo

        if not arquivo.exists():
            logger.warning(f"Não encontrado: {arquivo}")
            continue

        try:
            df = ler_finbra(arquivo)
            ferraz = filtrar_ferraz(df)

            if ferraz.empty:
                logger.warning(f"Ferraz não encontrada em {nome_arquivo} — {ano}")
                continue

            ferraz["ano"] = ano

            saida = PROCESSED_DIR / f"{nome_saida}_{ano}.csv"
            ferraz.to_csv(saida, index=False, encoding="utf-8-sig", sep=";", decimal=",")
            logger.success(f"Salvo: {saida.name} — {len(ferraz)} registros")

        except Exception as e:
            logger.error(f"Erro ao processar {nome_arquivo} — {ano}: {e}")

def main():
    pastas = sorted([p for p in RAW_DIR.iterdir() if p.is_dir()])

    if not pastas:
        logger.error(f"Nenhuma pasta encontrada em {RAW_DIR}")
        return

    for pasta in pastas:
        try:
            ano = int(pasta.name)
            processar_pasta(ano, pasta)
        except ValueError:
            logger.warning(f"Ignorada: {pasta.name}")

    logger.success("Processamento concluído!")
    logger.info(f"Arquivos em: {PROCESSED_DIR}")

if __name__ == "__main__":
    main()