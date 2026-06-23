import pandas as pd


df = pd.read_csv(
    "data/processed/tce_sp/ajustes_ferraz.csv",
    sep=";", encoding="utf-8-sig", dtype=str
)

casamax = df[
    df["CNPJ da empresa contratada"].str.replace(
        r"[.\-/]", "", regex=True
    ).str.strip() == "08183516000120"
]

# Adicione no início do script, antes do loop
print("Colunas disponíveis:")
print(casamax.columns.tolist())

print(f"Contratos CASAMAX encontrados: {len(casamax)}")
print()
for _, r in casamax.iterrows():
    print(f"Nº Contrato:  {r['Nº do contrato']}")
    print(f"Processo:     {r['Número do processo licitatório']}")
    print(f"Objeto:       {str(r['Objeto da licitação'])[:60]}")
    print(f"Descrição:    {str(r['Descrição do objeto contratado'])[:60]}")
    print(f"Valor:        {r['Valor total do contrato']}")
    print(f"Arquivo:      {r['arquivo_origem']}")
    print()