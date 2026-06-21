import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed/tce_sp")

adj = pd.read_csv(PROCESSED_DIR / "ajustes_ferraz.csv", sep=";", dtype=str, encoding="utf-8-sig")

casamax = adj[adj["CNPJ da empresa contratada"].str.replace(
    r"[.\-/]", "", regex=True).str.strip() == "08183516000120"].copy()

casamax["Valor total do contrato"] = pd.to_numeric(
    casamax["Valor total do contrato"].str.replace(",", "."), errors="coerce"
)

print("CASAMAX — detalhamento dos contratos:")
print(f"{'Arquivo':<35} {'Objeto':<35} {'Valor':>15}")
print("-" * 90)
for _, r in casamax.sort_values("Valor total do contrato", ascending=False).iterrows():
    arquivo = str(r["arquivo_origem"])[:33]
    objeto = str(r["Objeto da licitação"])[:33]
    valor = r["Valor total do contrato"]
    desc = str(r["Descrição do objeto da licitação"])[:80]
    print(f"{arquivo:<35} {objeto:<35} R$ {valor:>12,.2f}")
    print(f"  Desc: {desc}")
    print()