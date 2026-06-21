import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed/tce_sp")

df = pd.read_csv(
    PROCESSED_DIR / "datacity_analise.csv",
    sep=";", encoding="utf-8-sig", dtype=str
)

df["vl_despesa"] = df["vl_despesa"].str.replace(",", ".").astype(float)
df["ano_exercicio"] = df["ano_exercicio"].astype(int)
df["mes_referencia"] = pd.to_numeric(df["mes_referencia"], errors="coerce")

print("=" * 70)
print("DATACITY — LINHA DO TEMPO DE CONTRATOS E PAGAMENTOS")
print("=" * 70)

# Identifica contratos mencionados nos históricos
contratos = {
    "161/2016": [],
    "189/2021": [],
    "329/2022": [],
    "outros":   [],
}

for _, row in df.iterrows():
    hist = str(row.get("historico_despesa", "")).upper()
    if "161/16" in hist or "161/2016" in hist:
        contratos["161/2016"].append(row)
    elif "189/2021" in hist or "189/21" in hist:
        contratos["189/2021"].append(row)
    elif "329/2022" in hist or "329/22" in hist:
        contratos["329/2022"].append(row)
    else:
        contratos["outros"].append(row)

for nome, registros in contratos.items():
    if not registros:
        continue
    df_c = pd.DataFrame(registros)
    total = df_c["vl_despesa"].sum()
    anos = sorted(df_c["ano_exercicio"].unique())
    print(f"\n{'─'*70}")
    print(f"Contrato: {nome}")
    print(f"Total pago: R$ {total:,.2f}")
    print(f"Anos de vigência identificados: {anos}")
    print(f"Nº de empenhos: {len(df_c)}")
    print(f"\nDetalhamento:")
    for _, r in df_c.sort_values("ano_exercicio").iterrows():
        hist = str(r["historico_despesa"])[:70]
        print(f"  {int(r['ano_exercicio'])} | R$ {r['vl_despesa']:>14,.2f} | {hist}")

print(f"\n{'='*70}")
print(f"RESUMO")
print(f"{'='*70}")
for nome, registros in contratos.items():
    if registros:
        total = sum(r["vl_despesa"] for r in registros)
        print(f"  {nome:<15} {len(registros):>4} empenhos | R$ {total:>14,.2f}")