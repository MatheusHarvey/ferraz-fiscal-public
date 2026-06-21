import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw/transparencia_ferraz")
PROCESSED_DIR = Path("data/processed/transparencia_ferraz")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def ler_csv(caminho: Path) -> pd.DataFrame:
    return pd.read_csv(caminho, encoding="latin-1", sep="|")

# ── CASAMAX ──────────────────────────────────────────────
print("=" * 60)
print("CASAMAX — CONTRATOS")
print("=" * 60)

casamax = ler_csv(RAW_DIR / "casamax/lai_casamax.csv")
casamax = casamax[casamax["Ano"].notna()].copy()

for col in ["Valor Contratado", "Valor Empenhado", "Valor Pago"]:
    casamax[col] = pd.to_numeric(casamax[col], errors="coerce")

print(f"Total de contratos: {len(casamax)}")
print(f"Valor total contratado: R$ {casamax['Valor Contratado'].sum():,.2f}")
print(f"Valor total empenhado:  R$ {casamax['Valor Empenhado'].sum():,.2f}")
print(f"Valor total pago:       R$ {casamax['Valor Pago'].sum():,.2f}")

print(f"\nPor ano:")
print(casamax.groupby("Ano")["Valor Contratado"].sum().apply(
    lambda x: f"R$ {x:,.2f}").to_string())

print(f"\nObjetos:")
print(casamax["Objeto Contrato"].value_counts().head(10).to_string())

print(f"\nDetalhamento:")
for _, r in casamax.sort_values("Ano").iterrows():
    print(f"  {r['Ano']} | {r['Nro SIAM (Fiscalizadores)']} | "
          f"R$ {r['Valor Contratado']:>12,.2f} | R$ {r['Valor Pago']:>12,.2f} | "
          f"{str(r['Objeto Contrato'])[:50]}")

casamax.to_csv(PROCESSED_DIR / "casamax_contratos.csv",
               index=False, encoding="utf-8-sig", sep=";")

# ── DATACITY ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("DATACITY — CONTRATOS")
print("=" * 60)

datacity = ler_csv(RAW_DIR / "datacity/lai_Datacity.csv")
datacity = datacity[datacity["Ano"].notna()].copy()

for col in ["Valor Contratado", "Valor Empenhado", "Valor Pago"]:
    datacity[col] = pd.to_numeric(datacity[col], errors="coerce")

print(f"Total de contratos: {len(datacity)}")
print(f"Valor total contratado: R$ {datacity['Valor Contratado'].sum():,.2f}")
print(f"Valor total empenhado:  R$ {datacity['Valor Empenhado'].sum():,.2f}")
print(f"Valor total pago:       R$ {datacity['Valor Pago'].sum():,.2f}")

dif = datacity["Valor Empenhado"].sum() - datacity["Valor Contratado"].sum()
if dif > 0:
    print(f"\n🔴 Empenhado supera contratado em R$ {dif:,.2f}")

print(f"\nDetalhamento:")
for _, r in datacity.sort_values("Ano").iterrows():
    print(f"  {r['Ano']} | {r['Nro SIAM (Fiscalizadores)']} | "
          f"R$ {r['Valor Contratado']:>12,.2f} | R$ {r['Valor Pago']:>12,.2f} | "
          f"{str(r['Objeto Contrato'])[:50]}")

datacity.to_csv(PROCESSED_DIR / "datacity_contratos.csv",
                index=False, encoding="utf-8-sig", sep=";")

# ── EMENDAS ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("EMENDAS PARLAMENTARES")
print("=" * 60)

emendas_path = list(RAW_DIR.rglob("*emendas*.csv"))[0]
emendas = ler_csv(emendas_path)

for col in ["Orçado", "Empenhado", "Receita Recebida"]:
    if col in emendas.columns:
        emendas[col] = pd.to_numeric(emendas[col], errors="coerce")

print(f"Total de emendas: {len(emendas)}")
print(f"Valor orçado total:   R$ {emendas['Orçado'].sum():,.2f}")
print(f"Valor empenhado:      R$ {emendas['Empenhado'].sum():,.2f}")
print(f"Receita recebida:     R$ {emendas['Receita Recebida'].sum():,.2f}")

print(f"\nPor âmbito:")
print(emendas["Âmbito"].value_counts().to_string())

print(f"\nTop 10 parlamentares por valor orçado:")
top = emendas.groupby("Parlamentar")["Orçado"].sum().sort_values(ascending=False).head(10)
for parl, valor in top.items():
    print(f"  R$ {valor:>12,.2f}  {parl}")

emendas.to_csv(PROCESSED_DIR / "emendas_parlamentares.csv",
               index=False, encoding="utf-8-sig", sep=";")

print(f"\nArquivos salvos em: {PROCESSED_DIR}")
# Análise detalhada de emendas
print("\n--- Emendas por destinação ---")
print(emendas["Destinação"].value_counts().head(15).to_string())

print("\n--- Emendas com receita recebida > orçado ---")
emendas_suspeitas = emendas[emendas["Receita Recebida"] > emendas["Orçado"]]
print(f"Total: {len(emendas_suspeitas)}")
for _, r in emendas_suspeitas.iterrows():
    print(f"  Emenda {r['Nro Emenda']} | Orçado: R$ {r['Orçado']:,.2f} | "
          f"Recebido: R$ {r['Receita Recebida']:,.2f} | {str(r['Descrição'])[:60]}")

print("\n--- Emendas sem empenhamento (orçado mas não gasto) ---")
nao_empenhadas = emendas[
    (emendas["Orçado"] > 0) & (emendas["Empenhado"] == 0)
]
print(f"Total: {len(nao_empenhadas)} emendas orçadas mas não empenhadas")
print(f"Valor: R$ {nao_empenhadas['Orçado'].sum():,.2f}")