import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("../../data/processed/tce_sp")

# Limite legal de dispensa (Lei 8.666/93 Art. 24, II)
# Serviços e compras: R$ 17.600 | Obras: R$ 33.000
# Nova Lei 14.133/2021 (a partir de 2022): R$ 50.000 | Obras: R$ 100.000
LIMITE_SERVICOS = 50000
LIMITE_OBRAS = 100000

adj = pd.read_csv(
    PROCESSED_DIR / "ajustes_ferraz.csv",
    sep=";", dtype=str, encoding="utf-8-sig"
)

# Foca gestão atual e dispensas
gestao = adj[adj["arquivo_origem"].str.contains("2022|2023|2024", na=False)].copy()
dispensas = gestao[
    gestao["Modalidade de licitação"].str.contains("Dispensa", na=False)
].copy()

# Converte valores
dispensas["Valor total do contrato"] = pd.to_numeric(
    dispensas["Valor total do contrato"].str.replace(",", "."), errors="coerce"
)

# Extrai ano do arquivo de origem
dispensas["ano"] = dispensas["arquivo_origem"].str.extract(r"(\d{4})")

# Agrupa por fornecedor + ano
grupos = (
    dispensas.groupby(["Nome da empresa contratada", "CNPJ da empresa contratada", "ano"])
    .agg(
        qtd_contratos=("Valor total do contrato", "count"),
        valor_total=("Valor total do contrato", "sum"),
        valor_medio=("Valor total do contrato", "mean"),
        valor_maximo=("Valor total do contrato", "max"),
        objetos=("Objeto da licitação", lambda x: " | ".join(x.dropna().unique()[:3]))
    )
    .reset_index()
)

# Detecta suspeitos de fracionamento:
# - mais de 1 contrato no mesmo ano com mesmo fornecedor
# - soma ultrapassa o limite mas cada contrato individualmente está abaixo
suspeitos = grupos[
    (grupos["qtd_contratos"] > 1) &
    (grupos["valor_total"] > LIMITE_SERVICOS) &
    (grupos["valor_maximo"] < LIMITE_OBRAS)
].sort_values("valor_total", ascending=False)

print(f"Limite de dispensa aplicado: R$ {LIMITE_SERVICOS:,.2f} (serviços)")
print(f"Suspeitos de fracionamento (2022-2024): {len(suspeitos)}\n")
print("=" * 80)

for _, row in suspeitos.iterrows():
    print(f"Fornecedor: {row['Nome da empresa contratada']}")
    print(f"CNPJ:       {row['CNPJ da empresa contratada']}")
    print(f"Ano:        {row['ano']}")
    print(f"Contratos:  {int(row['qtd_contratos'])}x — soma R$ {row['valor_total']:,.2f} "
          f"(média R$ {row['valor_medio']:,.2f} cada)")
    print(f"Objetos:    {row['objetos']}")
    print("-" * 80)

# Salva
saida = PROCESSED_DIR / "suspeitos_fracionamento.csv"
suspeitos.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
print(f"\nTotal de casos suspeitos: {len(suspeitos)}")
print(f"Salvo em: {saida}")