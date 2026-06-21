import zipfile
import pandas as pd
from pathlib import Path
from loguru import logger
from io import StringIO

RAW_DIR = Path("../../data/raw/tce_sp/conjunto-dados/licitacoes-contratos")
PROCESSED_DIR = Path("../../data/processed/tce_sp")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

MUNICIPIO = "Ferraz de Vasconcelos"

def ler_csv_do_zip(zip_path: Path) -> pd.DataFrame | None:
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            csvs = [f for f in z.namelist() if f.endswith(".csv")]
            if not csvs:
                logger.warning(f"Sem CSV em {zip_path.name}")
                return None

            with z.open(csvs[0]) as f:
                conteudo = f.read().decode("latin-1")

            df = pd.read_csv(
                StringIO(conteudo),
                sep=";",
                dtype=str,
                quotechar='"',
            )
            return df

    except Exception as e:
        logger.error(f"Erro em {zip_path.name}: {e}")
        return None

def filtrar_ferraz(df: pd.DataFrame) -> pd.DataFrame:
    # Encontra a coluna de município independente de encoding
    col_municipio = next(
        (c for c in df.columns if "unic" in c.lower()),
        None
    )
    if not col_municipio:
        logger.warning("Coluna de município não encontrada")
        return pd.DataFrame()

    return df[df[col_municipio].str.strip() == MUNICIPIO].copy()

def main():
    zips = sorted(RAW_DIR.glob("*.zip"))
    logger.info(f"Total de ZIPs encontrados: {len(zips)}")

    licitacoes = []
    ajustes = []

    for zip_path in zips:
        logger.info(f"Processando {zip_path.name}...")
        df = ler_csv_do_zip(zip_path)

        if df is None or df.empty:
            continue

        ferraz = filtrar_ferraz(df)

        if ferraz.empty:
            logger.warning(f"Ferraz não encontrada em {zip_path.name}")
            continue

        ferraz["arquivo_origem"] = zip_path.name
        logger.success(f"{zip_path.name} — {len(ferraz)} registros de Ferraz")

        if zip_path.name.startswith("ajuste"):
            ajustes.append(ferraz)
        else:
            licitacoes.append(ferraz)

    # Salva licitações
    if licitacoes:
        df_lic = pd.concat(licitacoes, ignore_index=True)
        saida = PROCESSED_DIR / "licitacoes_ferraz.csv"
        df_lic.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
        logger.success(f"Licitações: {len(df_lic)} registros salvos")
        print(f"\nLicitações: {len(df_lic)} registros")
    else:
        print("\nNenhuma licitação encontrada para Ferraz")

    # Salva ajustes
    if ajustes:
        df_adj = pd.concat(ajustes, ignore_index=True)
        saida = PROCESSED_DIR / "ajustes_ferraz.csv"
        df_adj.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
        logger.success(f"Ajustes: {len(df_adj)} registros salvos")
        print(f"Ajustes/Contratos: {len(df_adj)} registros")
    else:
        print("Nenhum ajuste encontrado para Ferraz")

if __name__ == "__main__":
    main()