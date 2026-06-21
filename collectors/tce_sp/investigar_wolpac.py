import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed/tce_sp")

frames = []
for ano in [2020, 2021, 2022, 2023, 2024, 2025]:
    f = PROCESSED_DIR / f"despesas_tce_{ano}.csv"
    if f.exists():
        frames.append(pd.read_csv(f, sep=";", encoding="utf-8-sig", dtype=str))

df = pd.concat(frames, ignore_index=True)
df["vl_despesa"] = df["vl_despesa"].str.replace(",", ".").astype(float)

wolpac = df[
    (df["ds_despesa"].str.contains("WOLPAC", na=False)) &
    (df["tp_despesa"] == "Empenhado")
]

print(f"Total de empenhos WOLPAC: {len(wolpac)}")
print(f"Valor total: R$ {wolpac['vl_despesa'].sum():,.2f}")

print(f"\nPor ano:")
print(wolpac.groupby("ano_exercicio")["vl_despesa"].sum()
      .apply(lambda x: f"R$ {x:,.2f}").to_string())

print(f"\nModalidades:")
print(wolpac["ds_modalidade_lic"].value_counts().to_string())

print(f"\nFunções de governo:")
print(wolpac["ds_funcao_governo"].value_counts().to_string())

print(f"\nAmostra de históricos:")
for h in wolpac["historico_despesa"].dropna().head(5):
    print(f"  {str(h)[:120]}")

print(f"\nElementos de despesa:")
print(wolpac["ds_elemento"].value_counts().head(10).to_string())