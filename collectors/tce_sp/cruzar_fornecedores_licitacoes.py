import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed/tce_sp")

# Carrega licitações e ajustes
lic = pd.read_csv(PROCESSED_DIR / "licitacoes_ferraz.csv", sep=";", dtype=str, encoding="utf-8-sig")
adj = pd.read_csv(PROCESSED_DIR / "ajustes_ferraz.csv", sep=";", dtype=str, encoding="utf-8-sig")

# CNPJs alvo
alvos = {
    "DATACITY":  "02679522000197",
    "CASAMAX":   "08183516000120",
}

for nome, cnpj in alvos.items():
    print(f"\n{'='*70}")
    print(f"{nome} — CNPJ {cnpj}")
    print(f"{'='*70}")

    # Nos ajustes (contratos)
    adj_cnpj = adj[adj["CNPJ da empresa contratada"].str.replace(
        r"[.\-/]", "", regex=True).str.strip() == cnpj]

    print(f"\nContratos nos ajustes: {len(adj_cnpj)}")
    if not adj_cnpj.empty:
        adj_cnpj["Valor total do contrato"] = pd.to_numeric(
            adj_cnpj["Valor total do contrato"].str.replace(",", "."), errors="coerce"
        )
        print(f"Valor total: R$ {adj_cnpj['Valor total do contrato'].sum():,.2f}")
        print(f"\nModalidades:")
        print(adj_cnpj["Modalidade de licitação"].value_counts().to_string())
        print(f"\nObjetos:")
        for _, r in adj_cnpj.iterrows():
            print(f"  {r['arquivo_origem'][:30]} — {str(r['Objeto da licitação'])[:60]}")

    # Nas licitações (participações)
    lic_cnpj = lic[lic["CNPJ do participante candidato"].str.replace(
        r"[.\-/]", "", regex=True).str.strip() == cnpj]

    print(f"\nParticipações em licitações: {len(lic_cnpj)}")
    if not lic_cnpj.empty:
        print(f"Modalidades:")
        print(lic_cnpj["Modalidade de licitação"].value_counts().to_string())
        print(f"\nResultados de habilitação:")
        print(lic_cnpj["Resultado da Habilitação"].value_counts().to_string())