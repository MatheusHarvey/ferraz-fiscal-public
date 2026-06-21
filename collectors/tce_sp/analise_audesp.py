import pandas as pd
from pathlib import Path

RAW_DIR = Path("../../data/raw/tce_sp/conjunto-dados/resultado-analise")
PROCESSED_DIR = Path("../../data/processed/tce_sp")

df = pd.read_csv(
    RAW_DIR / "resultado_analises_audesp.csv",
    sep=";", encoding="latin-1", decimal=",", dtype=str,
)

# Filtra Ferraz
ferraz = df[df["Código IBGE"].astype(str).str.strip() == "3515707"].copy()

# Converte colunas numéricas
cols_pct = [
    "Despesa Empenhada Ensino (%)",
    "Despesa Empenhada Saúde (%)",
    "Despesa com Pessoal Poder Executivo (%)",
    "Despesa Empenhada FUNDEB (%)",
    "Resultado da Execução Orçamentária (%)",
]
# Converte colunas numéricas — substitui vírgula por ponto antes
for col in cols_pct:
    ferraz[col] = pd.to_numeric(
        ferraz[col].astype(str).str.replace(",", ".").str.strip(),
        errors="coerce"
    )

ferraz["Exercício"] = ferraz["Exercício"].astype(int)

# Limites constitucionais
MINIMO_ENSINO  = 0.25   # 25%
MINIMO_SAUDE   = 0.15   # 15%
LIMITE_PESSOAL = 0.54   # 54% LRF

print("=" * 70)
print("ANÁLISE DE CUMPRIMENTO DOS LIMITES CONSTITUCIONAIS — FERRAZ DE VASCONCELOS")
print("=" * 70)
print(f"\n{'Ano':<6} {'Ensino %':>9} {'Mín 25%':>8} {'Saúde %':>9} {'Mín 15%':>8} {'Pessoal %':>10} {'Lim 54%':>8}")
print("-" * 70)

alertas = []

for _, row in ferraz.sort_values("Exercício").iterrows():
    ano = int(row["Exercício"])
    ensino  = row["Despesa Empenhada Ensino (%)"]
    saude   = row["Despesa Empenhada Saúde (%)"]
    pessoal = row["Despesa com Pessoal Poder Executivo (%)"]

    flag_ensino  = "⚠" if pd.notna(ensino)  and ensino  < MINIMO_ENSINO  else "✓"
    flag_saude   = "⚠" if pd.notna(saude)   and saude   < MINIMO_SAUDE   else "✓"
    flag_pessoal = "⚠" if pd.notna(pessoal) and pessoal > LIMITE_PESSOAL else "✓"

    ensino_s  = f"{ensino*100:.1f}%  {flag_ensino}"  if pd.notna(ensino)  else "  s/d"
    saude_s   = f"{saude*100:.1f}%  {flag_saude}"   if pd.notna(saude)   else "  s/d"
    pessoal_s = f"{pessoal*100:.1f}% {flag_pessoal}" if pd.notna(pessoal) else "  s/d"

    print(f"{ano:<6} {ensino_s:>14} {'':>3} {saude_s:>14} {'':>3} {pessoal_s:>14}")

    if flag_ensino == "⚠":
        alertas.append(f"{ano}: Ensino abaixo do mínimo ({ensino*100:.1f}% < 25%)")
    if flag_saude == "⚠":
        alertas.append(f"{ano}: Saúde abaixo do mínimo ({saude*100:.1f}% < 15%)")
    if flag_pessoal == "⚠":
        alertas.append(f"{ano}: Pessoal acima do limite ({pessoal*100:.1f}% > 54%)")

print("-" * 70)

if alertas:
    print(f"\n🔴 ALERTAS IDENTIFICADOS ({len(alertas)}):")
    for a in alertas:
        print(f"  • {a}")
else:
    print("\n✅ Nenhuma violação de limite constitucional identificada.")

# Salva processado
saida = PROCESSED_DIR / "audesp_ferraz.csv"
ferraz.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
print(f"\nSalvo em: {saida}")