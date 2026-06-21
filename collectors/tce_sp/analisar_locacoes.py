import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("../../data/processed/tce_sp")

# Carrega ajustes
adj = pd.read_csv(PROCESSED_DIR / "ajustes_ferraz.csv", sep=";", dtype=str, encoding="utf-8-sig")

# Filtra locações de imóveis por dispensa
locacoes = adj[
    (adj["Objeto da licitação"].str.contains("Loca", na=False, case=False)) &
    (adj["Modalidade de licitação"].str.contains("Dispensa", na=False))
].copy()

# Converte valor
locacoes["Valor total do contrato"] = pd.to_numeric(
    locacoes["Valor total do contrato"].str.replace(",", "."), errors="coerce"
)

print(f"Total de locações por dispensa: {len(locacoes)}")
print(f"\nColunas disponíveis:")
for c in locacoes.columns:
    print(f"  '{c}'")

print(f"\nAmostra:")
print(locacoes[[
    "arquivo_origem",
    "Objeto da licitação",
    "Descrição do objeto da licitação",
    "Nome da empresa contratada",
    "CNPJ da empresa contratada",
    "Valor total do contrato",
    "Vigência do contrato - Data início",
    "Vigência do contrato - Data Término",
]].to_string())

# Análise aprofundada
print("\n" + "=" * 70)
print("ANÁLISE DE LOCAÇÕES DE IMÓVEIS POR DISPENSA")
print("=" * 70)

total = locacoes["Valor total do contrato"].sum()
print(f"\nValor total das locações: R$ {total:,.2f}")
print(f"Valor médio por contrato: R$ {locacoes['Valor total do contrato'].mean():,.2f}")

# Pessoas físicas vs jurídicas
pf = locacoes[locacoes["CNPJ da empresa contratada"].isna()]
pj = locacoes[locacoes["CNPJ da empresa contratada"].notna()]
print(f"\nPessoas físicas: {len(pf)} contratos — R$ {pf['Valor total do contrato'].sum():,.2f}")
print(f"Pessoas jurídicas: {len(pj)} contratos — R$ {pj['Valor total do contrato'].sum():,.2f}")

# Detecta possíveis vínculos familiares (mesmo sobrenome)
print("\n--- Possíveis vínculos familiares (mesmo sobrenome) ---")
locacoes["sobrenome"] = locacoes["Nome da empresa contratada"].str.strip().str.split().str[-1]
sobrenomes = locacoes.groupby("sobrenome").filter(lambda x: len(x) > 1)
if not sobrenomes.empty:
    for sobrenome, grupo in sobrenomes.groupby("sobrenome"):
        valor_grupo = grupo["Valor total do contrato"].sum()
        print(f"\nSobrenome '{sobrenome}':")
        for _, r in grupo.iterrows():
            print(f"  {r['Nome da empresa contratada']} — R$ {r['Valor total do contrato']:,.2f} "
                  f"({r['arquivo_origem'].split('-')[1] if '-' in r['arquivo_origem'] else ''})")
        print(f"  TOTAL: R$ {valor_grupo:,.2f}")

# Contratos mais altos
print("\n--- Top 5 maiores contratos ---")
top = locacoes.nlargest(5, "Valor total do contrato")
for _, r in top.iterrows():
    print(f"  R$ {r['Valor total do contrato']:,.2f} — {r['Nome da empresa contratada']} "
          f"({r['Vigência do contrato - Data início']} a {r['Vigência do contrato - Data Término']})")

# Salva
saida = PROCESSED_DIR / "locacoes_imoveis.csv"
locacoes.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
print(f"\nSalvo em: {saida}")