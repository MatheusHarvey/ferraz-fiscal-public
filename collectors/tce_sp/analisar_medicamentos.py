import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("../../data/processed/tce_sp")

lic = pd.read_csv(
    PROCESSED_DIR / "licitacoes_ferraz.csv",
    sep=";", dtype=str, encoding="utf-8-sig"
)
adj = pd.read_csv(
    PROCESSED_DIR / "ajustes_ferraz.csv",
    sep=";", dtype=str, encoding="utf-8-sig"
)

# Filtra medicamentos nas licitações
med_lic = lic[
    (lic["Objeto"].str.contains("Medicamento", na=False, case=False)) &
    (lic["Modalidade de licitação"].str.contains("Dispensa", na=False))
].copy()

# Filtra medicamentos nos ajustes
med_adj = adj[
    (adj["Objeto da licitação"].str.contains("Medicamento", na=False, case=False)) &
    (adj["Modalidade de licitação"].str.contains("Dispensa", na=False))
].copy()

# Converte valores
med_adj["Valor total do contrato"] = pd.to_numeric(
    med_adj["Valor total do contrato"].str.replace(",", "."), errors="coerce"
)
med_lic["Valor da Proposta"] = pd.to_numeric(
    med_lic["Valor da Proposta"].str.replace(",", "."), errors="coerce"
)

print(f"Dispensas de medicamentos nas licitações: {len(med_lic)}")
print(f"Dispensas de medicamentos nos ajustes: {len(med_adj)}")

# Analisa por ano
print("\n--- Dispensas por ano (licitações) ---")
med_lic["ano"] = med_lic["arquivo_origem"].str.extract(r"(\d{4})")
print(med_lic.groupby("ano").size().to_string())

# Fornecedores mais frequentes nas licitações
print("\n--- Top 15 participantes nas dispensas de medicamentos ---")
print(med_lic["Nome do participante candidato"].value_counts().head(15).to_string())

# Contratos de medicamentos nos ajustes
print(f"\n--- Contratos de medicamentos nos ajustes ---")
print(f"Total de contratos: {len(med_adj)}")
if len(med_adj) > 0:
    print(f"Valor total: R$ {med_adj['Valor total do contrato'].sum():,.2f}")
    print(f"\nTop fornecedores por valor:")
    top = (
        med_adj.groupby("Nome da empresa contratada")["Valor total do contrato"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    for nome, valor in top.items():
        print(f"  R$ {valor:>14,.2f}  {nome}")

# Salva
saida = PROCESSED_DIR / "medicamentos_dispensas.csv"
med_lic.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
print(f"\nSalvo em: {saida}")

# Adicione ao final do analisar_medicamentos.py

print("\n--- Investigando o salto de 2024 ---")
med_2024 = med_lic[med_lic["ano"] == "2024"].copy()
med_outros = med_lic[med_lic["ano"] != "2024"].copy()

print(f"Média anual 2020-2023: {len(med_outros)/4:.0f} dispensas")
print(f"Total 2024: {len(med_2024)} dispensas")
print(f"Variação: +{len(med_2024)/(len(med_outros)/4)*100:.0f}%")

# Objetos mais frequentes em 2024
print(f"\nDescrições mais frequentes em 2024:")
print(med_2024["Descrição do objeto contratado"].value_counts().head(15).to_string())

# Verifica se há meses de pico em 2024
print(f"\nDisponibilidade por arquivo em 2024:")
print(med_2024["arquivo_origem"].value_counts().to_string())

print("\n--- Detalhando março e dezembro de 2024 ---")

for arquivo in ["licitacao-2024-03_0.zip", "licitacao-2024-12_0.zip"]:
    mes = med_2024[med_2024["arquivo_origem"] == arquivo]
    print(f"\n{arquivo}: {len(mes)} dispensas")

    # Códigos de licitação únicos — são processos distintos ou o mesmo?
    cod_col = "Código da Licitação"
    if cod_col in mes.columns:
        codigos = mes[cod_col].nunique()
        print(f"  Processos licitatórios distintos: {codigos}")
        print(f"  Top 5 processos com mais itens:")
        print(mes[cod_col].value_counts().head(5).to_string())

    # Entidades contratantes
    if "Entidade" in mes.columns:
        print(f"  Entidades:")
        print(mes["Entidade"].value_counts().to_string())