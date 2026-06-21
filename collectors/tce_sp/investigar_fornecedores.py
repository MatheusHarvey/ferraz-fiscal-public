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

# Foca em empenhos
emp = df[df["tp_despesa"] == "Empenhado"].copy()

for nome_busca in ["CASAMAX", "DATACITY"]:
    fornecedor = emp[emp["ds_despesa"].str.contains(nome_busca, na=False)]

    print(f"\n{'='*70}")
    print(f"FORNECEDOR: {nome_busca}")
    print(f"{'='*70}")
    print(f"Total de empenhos: {len(fornecedor)}")
    print(f"Valor total: R$ {fornecedor['vl_despesa'].sum():,.2f}")

    print(f"\nPor ano:")
    print(fornecedor.groupby("ano_exercicio")["vl_despesa"]
          .sum().apply(lambda x: f"R$ {x:,.2f}").to_string())

    print(f"\nModalidades de licitação:")
    print(fornecedor["ds_modalidade_lic"].value_counts().to_string())

    print(f"\nFunções de governo:")
    print(fornecedor["ds_funcao_governo"].value_counts().to_string())

    print(f"\nElementos de despesa (top 10):")
    print(fornecedor["ds_elemento"].value_counts().head(10).to_string())

    print(f"\nAmostra de históricos:")
    for h in fornecedor["historico_despesa"].dropna().head(8):
        print(f"  {str(h)[:120]}")

    # CNPJ
    cnpjs = fornecedor["nr_identificador_despesa"].value_counts()
    print(f"\nCNPJs identificados:")
    print(cnpjs.to_string())