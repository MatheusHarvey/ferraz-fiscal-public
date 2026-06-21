import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw/datasus")
PROCESSED_DIR = Path("data/processed/datasus")
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Dados extraídos dos CSVs do TABNET
obitos_ano = pd.DataFrame([
    {"ano": 2020, "obitos": 1223},
    {"ano": 2021, "obitos": 1532},
    {"ano": 2022, "obitos": 1173},
    {"ano": 2023, "obitos": 1129},
    {"ano": 2024, "obitos": 1197},
])

obitos_causa = pd.DataFrame([
    {"causa": "Doenças do aparelho circulatório",   "obitos": 1414, "capitulo": "IX"},
    {"causa": "Neoplasias (tumores)",                "obitos": 856,  "capitulo": "II"},
    {"causa": "Sint/sinais e achados anormais",      "obitos": 854,  "capitulo": "XVIII"},
    {"causa": "Doenças infecciosas e parasitárias",  "obitos": 792,  "capitulo": "I"},
    {"causa": "Doenças do aparelho respiratório",    "obitos": 625,  "capitulo": "X"},
    {"causa": "Causas externas",                     "obitos": 419,  "capitulo": "XX"},
    {"causa": "Doenças endócrinas e metabólicas",    "obitos": 361,  "capitulo": "IV"},
    {"causa": "Doenças do aparelho digestivo",       "obitos": 269,  "capitulo": "XI"},
    {"causa": "Doenças do aparelho geniturinário",   "obitos": 219,  "capitulo": "XIV"},
    {"causa": "Doenças do sistema nervoso",          "obitos": 168,  "capitulo": "VI"},
    {"causa": "Afecções perinatais",                 "obitos": 94,   "capitulo": "XVI"},
    {"causa": "Transtornos mentais",                 "obitos": 46,   "capitulo": "V"},
    {"causa": "Doenças do sangue",                   "obitos": 45,   "capitulo": "III"},
    {"causa": "Doenças da pele",                     "obitos": 36,   "capitulo": "XII"},
    {"causa": "Malformações congênitas",             "obitos": 31,   "capitulo": "XVII"},
    {"causa": "Gravidez e parto",                    "obitos": 13,   "capitulo": "XV"},
    {"causa": "Doenças osteomusculares",             "obitos": 11,   "capitulo": "XIII"},
    {"causa": "Doenças do ouvido",                   "obitos": 1,    "capitulo": "VIII"},
])

# População estimada para cálculo de taxas
POPULACAO = 186479

# Calcula taxa de mortalidade por 100 mil habitantes
obitos_ano["taxa_por_100k"] = (obitos_ano["obitos"] / POPULACAO * 100000).round(1)
obitos_causa["pct_total"] = (obitos_causa["obitos"] / 6254 * 100).round(1)

# Salva
obitos_ano.to_csv(PROCESSED_DIR / "obitos_por_ano.csv", index=False, encoding="utf-8-sig", sep=";")
obitos_causa.to_csv(PROCESSED_DIR / "obitos_por_causa.csv", index=False, encoding="utf-8-sig", sep=";")

print("=" * 60)
print("DATASUS — MORTALIDADE FERRAZ DE VASCONCELOS 2020-2024")
print("=" * 60)
print(f"\nTotal de óbitos: 6.254")
print(f"População estimada: {POPULACAO:,}")
print(f"Taxa média: {6254/5/POPULACAO*100000:.1f} óbitos por 100 mil hab/ano")

print(f"\n--- Evolução anual ---")
for _, r in obitos_ano.iterrows():
    barra = "█" * int(r["obitos"] / 50)
    print(f"  {int(r['ano'])}: {int(r['obitos']):>5} óbitos ({r['taxa_por_100k']:.1f}/100k)  {barra}")

print(f"\n--- Top 5 causas ---")
for _, r in obitos_causa.nlargest(5, "obitos").iterrows():
    print(f"  {r['causa']:<40} {int(r['obitos']):>5} ({r['pct_total']:.1f}%)")

print(f"\n--- Causas externas ---")
ext = obitos_causa[obitos_causa["capitulo"] == "XX"].iloc[0]
print(f"  Causas externas (violência, acidentes): {int(ext['obitos'])} óbitos ({ext['pct_total']:.1f}%)")
print(f"  = {ext['obitos']/5:.0f} mortes por causas externas por ano em média")

print(f"\nArquivos salvos em: {PROCESSED_DIR}")