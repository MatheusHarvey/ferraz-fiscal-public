import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw/transparencia_ferraz")

def ler_csv(caminho: Path) -> pd.DataFrame:
    for enc in ["utf-8-sig", "latin-1", "utf-8"]:
        for sep in [";", ",", "\t"]:
            try:
                df = pd.read_csv(caminho, encoding=enc, sep=sep)
                if len(df.columns) > 3:
                    return df
            except:
                continue
    return pd.DataFrame()

# Inspeciona CASAMAX
print("CASAMAX — estrutura bruta:")
casamax_raw = ler_csv(RAW_DIR / "casamax/lai_casamax.csv")
print(f"Separador detectado | Colunas: {len(casamax_raw.columns)}")
print(casamax_raw.columns.tolist())
print("\nPrimeiras 3 linhas brutas:")
print(casamax_raw.head(3).to_string())

print("\n\nDATACITY — estrutura bruta:")
datacity_raw = ler_csv(RAW_DIR / "datacity/lai_Datacity.csv")
print(f"Colunas: {len(datacity_raw.columns)}")
print(datacity_raw.columns.tolist())
print("\nPrimeiras 3 linhas brutas:")
print(datacity_raw.head(3).to_string())