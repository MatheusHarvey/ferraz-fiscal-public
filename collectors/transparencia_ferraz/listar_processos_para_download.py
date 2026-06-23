import pandas as pd
from pathlib import Path

TCE_DIR = Path("data/processed/tce_sp")
PORTAL_DIR = Path("data/processed/transparencia_ferraz")

print("=" * 70)
print("PROCESSOS PARA DOWNLOAD DE ITENS — PORTAL TRANSPARÊNCIA FERRAZ")
print("=" * 70)

# ── CASAMAX ──────────────────────────────────────────────────────────
print("\n🔴 CASAMAX (CNPJ: 08.183.516/0001-20)")
print("-" * 70)

casamax_portal = pd.read_csv(
    PORTAL_DIR / "casamax_contratos.csv",
    sep=";", encoding="utf-8-sig", dtype=str
)
casamax_portal = casamax_portal[casamax_portal["Ano"].notna()]

print(f"\n{'Nro SIAM':<20} {'Ano':<6} {'Tipo':<30} {'Objeto':<30}")
print("-" * 90)
for _, r in casamax_portal.sort_values("Ano").iterrows():
    siam = str(r.get("Nro SIAM (Fiscalizadores)", "")).strip()
    ano = str(r.get("Ano", "")).strip()
    tipo = str(r.get("Tipo", "")).strip()[:28]
    obj = str(r.get("Objeto Contrato", "")).strip()[:28]
    print(f"  {siam:<18} {ano:<6} {tipo:<30} {obj}")

# ── DATACITY ─────────────────────────────────────────────────────────
print("\n\n🔵 DATACITY (CNPJ: 02.679.522/0001-97)")
print("-" * 70)

datacity_portal = pd.read_csv(
    PORTAL_DIR / "datacity_contratos.csv",
    sep=";", encoding="utf-8-sig", dtype=str
)
datacity_portal = datacity_portal[datacity_portal["Ano"].notna()]

print(f"\n{'Nro SIAM':<20} {'Ano':<6} {'Tipo':<30} {'Objeto':<30}")
print("-" * 90)
for _, r in datacity_portal.sort_values("Ano").iterrows():
    siam = str(r.get("Nro SIAM (Fiscalizadores)", "")).strip()
    ano = str(r.get("Ano", "")).strip()
    tipo = str(r.get("Tipo", "")).strip()[:28]
    obj = str(r.get("Objeto Contrato", "")).strip()[:28]
    print(f"  {siam:<18} {ano:<6} {tipo:<30} {obj}")

# ── Processos do TCE-SP ───────────────────────────────────────────────
print("\n\n📋 PROCESSOS LICITATÓRIOS — TCE-SP (ajustes)")
print("-" * 70)

ajustes = pd.read_csv(
    TCE_DIR / "ajustes_ferraz.csv",
    sep=";", encoding="utf-8-sig", dtype=str
)

for nome, cnpj in [("CASAMAX", "08183516000120"), ("DATACITY", "02679522000197")]:
    df = ajustes[
        ajustes["CNPJ da empresa contratada"].str.replace(
            r"[.\-/]", "", regex=True
        ).str.strip() == cnpj
    ]
    print(f"\n{nome}:")
    print(f"  {'Nº Contrato':<15} {'Processo Licitatório':<25} {'Objeto':<40}")
    print(f"  {'-'*80}")
    for _, r in df.iterrows():
        contrato = str(r.get("Nº do contrato", "")).strip()
        processo = str(r.get("Número do processo licitatório", "")).strip()
        objeto = str(r.get("Objeto da licitação", "")).strip()[:38]
        print(f"  {contrato:<15} {processo:<25} {objeto}")

print("\n\n💡 COMO USAR NO PORTAL:")
print("  1. Acesse: transparencia.ferrazdevasconcelos.sp.gov.br")
print("  2. Menu: Compras/Licitações")
print("  3. Filtre por Nro Processo Licitatório ou Nro Processo Adm")
print("  4. Clique em 'Compras por Itens' para ver os itens detalhados")
print("  5. Exporte como Excel/CSV")