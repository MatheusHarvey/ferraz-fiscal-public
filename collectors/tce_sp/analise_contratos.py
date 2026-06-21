import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("../../data/processed/tce_sp")

adj = pd.read_csv(PROCESSED_DIR / "ajustes_ferraz.csv", sep=";", dtype=str, encoding="utf-8-sig")

# Foca na gestão atual
gestao = adj[adj["arquivo_origem"].str.contains("2022|2023|2024", na=False)].copy()

# Converte valor para número
gestao["Valor total do contrato"] = pd.to_numeric(
    gestao["Valor total do contrato"].str.replace(",", "."), errors="coerce"
)

# Só dispensas
dispensas = gestao[
    gestao["Modalidade de licitação"].str.contains("Dispensa", na=False)
].copy()

print(f"Total de contratos por dispensa (2022-2024): {len(dispensas)}")

# Top fornecedores por valor
print("\nTop 15 fornecedores por valor total recebido (dispensas):")
top_valor = (
    dispensas.groupby("Nome da empresa contratada")["Valor total do contrato"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)
for nome, valor in top_valor.items():
    print(f"  R$ {valor:>14,.2f}  {nome}")

# Top fornecedores por frequência
print("\nTop 15 fornecedores por número de contratos (dispensas):")
top_freq = (
    dispensas["Nome da empresa contratada"]
    .value_counts()
    .head(15)
)
for nome, qtd in top_freq.items():
    print(f"  {qtd:>4}x  {nome}")

# Valor total movimentado por dispensa
total = dispensas["Valor total do contrato"].sum()
print(f"\nValor total movimentado por dispensa (2022-2024): R$ {total:,.2f}")

# Salva resultado
saida = PROCESSED_DIR / "contratos_dispensas_2022_2024.csv"
dispensas.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
print(f"\nSalvo em: {saida}")