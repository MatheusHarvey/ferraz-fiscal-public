import pandas as pd
from pathlib import Path

RAW_DIR = Path("../../data/raw/portal_federal")
PROCESSED_DIR = Path("../../data/processed/portal_federal")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_DIR / "convenios_ferraz.csv", sep=";", encoding="utf-8-sig")

# Filtra excluindo os status regulares em vez de incluir por nome
regulares = ["EM EXECUÇÃO", "NORMAL", "CONCLUÍDO"]
alertas = df[~df["situacao"].isin(regulares)].copy()

colunas = [
    "situacao",
    "dimConvenio.objeto",
    "dimConvenio.numero",
    "dataInicioVigencia",
    "dataFinalVigencia",
    "valor",
    "valorLiberado",
    "orgao.nome",
]

resultado = alertas[colunas].sort_values("situacao")

saida = PROCESSED_DIR / "convenios_alertas.csv"
resultado.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")

print(f"Total de convênios com alerta: {len(resultado)}\n")
for _, row in resultado.iterrows():
    print(f"{'='*60}")
    print(f"Situação:  {row['situacao']}")
    print(f"Objeto:    {row['dimConvenio.objeto']}")
    print(f"Convênio:  {row['dimConvenio.numero']}")
    print(f"Período:   {row['dataInicioVigencia']} até {row['dataFinalVigencia']}")
    print(f"Valor:     R$ {row['valor']:,.2f}")
    print(f"Liberado:  R$ {row['valorLiberado']:,.2f}")
    print(f"Órgão:     {row['orgao.nome']}")
print(f"{'='*60}")
print(f"\nSalvo em: {saida}")