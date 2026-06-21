import pandas as pd
from pathlib import Path
from datetime import date

PROCESSED_DIR = Path("data/processed/tce_sp")
DOCS_DIR = Path("docs")

frames = []
for ano in [2020, 2021, 2022, 2023, 2024, 2025]:
    f = PROCESSED_DIR / f"despesas_tce_{ano}.csv"
    if f.exists():
        frames.append(pd.read_csv(f, sep=";", encoding="utf-8-sig", dtype=str))

df = pd.concat(frames, ignore_index=True)
df["vl_despesa"] = df["vl_despesa"].str.replace(",", ".").astype(float)

datacity = df[
    (df["ds_despesa"].str.contains("DATACITY", na=False)) &
    (df["tp_despesa"] == "Empenhado")
].copy()

# Resumo por ano
por_ano = datacity.groupby("ano_exercicio")["vl_despesa"].sum()

# Identifica contratos pelo histórico
datacity["contrato"] = datacity["historico_despesa"].str.extract(
    r"(CT\.?\s*\d+/\d+|CONTRATO\s*N?\.?\s*\d+/\d+|CONTRATO\s*\d+/\d+)",
    expand=False, flags=2
)

# Indenizações
indenizacoes = datacity[
    datacity["historico_despesa"].str.contains("INDENIZ|AJUSTE|AJUSTES|REEMPENHO", na=False, case=False)
]

print("=" * 70)
print("DATACITY — ANÁLISE DE CONTRATOS")
print("=" * 70)
print(f"\nCNPJ: 02.679.522/0001-97")
print(f"Total empenhos: {len(datacity)}")
print(f"Valor total 2020-2025: R$ {datacity['vl_despesa'].sum():,.2f}")

print(f"\nEvolução anual:")
for ano, valor in por_ano.items():
    barra = "█" * int(valor / 500000)
    print(f"  {ano}: R$ {valor:>14,.2f}  {barra}")

print(f"\nIndenizações e termos de ajuste:")
print(f"  Total: {len(indenizacoes)} ocorrências — R$ {indenizacoes['vl_despesa'].sum():,.2f}")

print(f"\nContratos identificados:")
contratos = datacity["contrato"].dropna().value_counts()
print(contratos.to_string())

# Salva CSV de análise
saida = PROCESSED_DIR / "datacity_analise.csv"
datacity.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
print(f"\nSalvo em: {saida}")