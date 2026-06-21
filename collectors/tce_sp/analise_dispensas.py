import pandas as pd

df = pd.read_csv(
    "../../data/processed/tce_sp/licitacoes_ferraz.csv",
    sep=";",
    dtype=str,
    encoding="utf-8-sig"
)

# Mostra colunas disponíveis
print("Colunas disponíveis:")
for c in df.columns:
    print(f"  '{c}'")

# Filtra gestão atual e dispensas
gestao_atual = df[df["arquivo_origem"].str.contains("2022|2023|2024", na=False)]
col_modal = "Modalidade de licitação"

dispensas = gestao_atual[
    gestao_atual[col_modal].str.contains("Dispensa", na=False)
]

print(f"\nTotal de dispensas (2022-2024): {len(dispensas)}")
print(f"\nTop 15 fornecedores nas dispensas:")
print(dispensas["Nome do participante candidato"].value_counts().head(15).to_string())

# Verifica quais colunas têm dados nas dispensas
print("\nColunas com dados preenchidos nas dispensas:")
for col in dispensas.columns:
    nao_nulos = dispensas[col].notna().sum()
    if nao_nulos > 0:
        print(f"  {col}: {nao_nulos} registros preenchidos")

# Top objetos das dispensas
print(f"\nTop 15 objetos mais frequentes nas dispensas:")
print(dispensas["Objeto"].value_counts().head(15).to_string())