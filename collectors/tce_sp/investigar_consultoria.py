import pandas as pd

df = pd.read_csv(
    "data/processed/tce_sp/licitacoes_ferraz.csv",
    sep=";", encoding="utf-8-sig", dtype=str
)

consultoria = df[
    df["Objeto"].str.contains("CONSULTORIA|CONSULTIVA|ASSESSORIA", na=False, case=False)
].drop_duplicates("Objeto")

print(f"Total de dispensas de consultoria: {len(consultoria)}")
print()

for _, r in consultoria.iterrows():
    print(f"Arquivo:     {r['arquivo_origem']}")
    print(f"Modalidade:  {r['Modalidade de licitação']}")
    print(f"Objeto:      {r['Objeto']}")
    print(f"Descrição:   {str(r['Descrição do objeto contratado'])[:100]}")
    print(f"Proposta:    {r['Valor da Proposta']}")
    print(f"Fornecedor:  {r['Nome do participante candidato']}")
    print()

    import pandas as pd

# Busca nos ajustes
adj = pd.read_csv(
    "data/processed/tce_sp/ajustes_ferraz.csv",
    sep=";", encoding="utf-8-sig", dtype=str
)

consultoria_adj = adj[
    adj["Objeto da licitação"].str.contains(
        "CONSULTORIA|CONSULTIVA|ASSESSORIA", na=False, case=False
    )
]

print(f"Consultoria nos ajustes: {len(consultoria_adj)}")
print()
for _, r in consultoria_adj.iterrows():
    print(f"Arquivo:    {r['arquivo_origem']}")
    print(f"Contrato:   {r['Nº do contrato']}")
    print(f"Objeto:     {r['Objeto da licitação']}")
    print(f"Descrição:  {str(r['Descrição do objeto contratado'])[:100]}")
    print(f"Valor:      {r['Valor total do contrato']}")
    print(f"Fornecedor: {r['Nome da empresa contratada']}")
    print(f"CNPJ:       {r['CNPJ da empresa contratada']}")
    print()