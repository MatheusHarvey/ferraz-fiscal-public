import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("../../data/processed/tce_sp")

# Carrega os dois arquivos
lic = pd.read_csv(PROCESSED_DIR / "licitacoes_ferraz.csv", sep=";", dtype=str, encoding="utf-8-sig")
adj = pd.read_csv(PROCESSED_DIR / "ajustes_ferraz.csv", sep=";", dtype=str, encoding="utf-8-sig")

print("Colunas em ajustes_ferraz.csv:")
for c in adj.columns:
    print(f"  '{c}'")

print(f"\nTotal ajustes: {len(adj)}")
print(f"\nAmostra de ajustes 2022+:")
adj_recentes = adj[adj["arquivo_origem"].str.contains("2022|2023|2024", na=False)]
print(f"Ajustes 2022-2024: {len(adj_recentes)}")
print(adj_recentes.head(3).to_string())