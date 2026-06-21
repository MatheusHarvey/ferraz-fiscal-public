import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed/ibge")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

dados = [
    {"indicador": "populacao_censo",          "valor": 179198,     "ano": 2022, "unidade": "pessoas"},
    {"indicador": "populacao_estimada",        "valor": 186479,     "ano": 2025, "unidade": "pessoas"},
    {"indicador": "densidade_demografica",     "valor": 6064.85,    "ano": 2022, "unidade": "hab/km²"},
    {"indicador": "pib_per_capita",            "valor": 30826.13,   "ano": 2023, "unidade": "R$"},
    {"indicador": "idhm",                      "valor": 0.738,      "ano": 2010, "unidade": "índice"},
    {"indicador": "salario_medio_formal",      "valor": 2.5,        "ano": 2023, "unidade": "salários mínimos"},
    {"indicador": "empregos_formais",          "valor": 28062,      "ano": 2023, "unidade": "pessoas"},
    {"indicador": "pop_ate_meio_sm",           "valor": 37.0,       "ano": 2010, "unidade": "%"},
    {"indicador": "escolarizacao_6_14",        "valor": 98.26,      "ano": 2022, "unidade": "%"},
    {"indicador": "ideb_fundamental_inicial",  "valor": 6.1,        "ano": 2023, "unidade": "nota"},
    {"indicador": "ideb_fundamental_final",    "valor": 5.0,        "ano": 2023, "unidade": "nota"},
    {"indicador": "mortalidade_infantil",      "valor": 13.6,       "ano": 2023, "unidade": "por mil nascidos"},
    {"indicador": "esgotamento_sanitario",     "valor": 88.54,      "ano": 2022, "unidade": "%"},
    {"indicador": "urbanizacao_vias",          "valor": 11.8,       "ano": 2010, "unidade": "%"},
    {"indicador": "area_km2",                  "valor": 29.58,      "ano": 2025, "unidade": "km²"},
    {"indicador": "receita_total",             "valor": 732618633.68, "ano": 2024, "unidade": "R$"},
    {"indicador": "despesa_total_empenhada",   "valor": 652083105.99, "ano": 2024, "unidade": "R$"},
    {"indicador": "transferencias_correntes_pct", "valor": 70.49,  "ano": 2024, "unidade": "%"},
]

df = pd.DataFrame(dados)
saida = PROCESSED_DIR / "ibge_ferraz.csv"
df.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")

print(f"Salvo: {saida}")
print(f"Total de indicadores: {len(df)}")
print(f"\nDestaques para o projeto:")
print(f"  PIB per capita: R$ {30826.13:,.2f} (2023)")
print(f"  IDHM: 0,738 (2010 — dado desatualizado)")
print(f"  Urbanização de vias: 11,8% (2010) — contexto das obras de pavimentação")
print(f"  Pop. até 1/2 SM: 37% (2010) — contexto do gasto com tecnologia")
print(f"  Transferências correntes: 70,49% da receita — alta dependência de repasses")