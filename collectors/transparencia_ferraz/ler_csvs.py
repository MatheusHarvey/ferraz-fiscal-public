import pandas as pd
from pathlib import Path

p = Path("data/raw/transparencia_ferraz")
csvs = list(p.rglob("*.csv"))
print(f"CSVs encontrados: {len(csvs)}")

for csv in csvs:
    print("\n" + "=" * 60)
    print(f"Arquivo: {csv.name}")
    for enc in ["utf-8-sig", "latin-1", "utf-8"]:
        try:
            df = pd.read_csv(csv, encoding=enc, sep=None, engine="python")
            print(f"Linhas: {len(df)} | Colunas: {list(df.columns)}")
            print(df.head(2).to_string())
            break
        except Exception as e:
            continue