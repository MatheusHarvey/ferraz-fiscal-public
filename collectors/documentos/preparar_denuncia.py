import shutil
from pathlib import Path

BASE = Path("denuncia_tce_sp")
DOCS = BASE / "documentos"
ANEXOS = BASE / "anexos"

PROCESSED = Path("data/processed")
RAW = Path("data/raw")
DOCS_DIR = Path("docs")

print("Preparando pasta de denúncia...")
print()

# ── Documentos principais ──────────────────────────────────────────────
copias_docs = [
    (DOCS_DIR / "resumo_executivo_tce_sp.md",
     DOCS / "01_resumo_executivo.md"),
    (DOCS_DIR / "relatorio_irregularidades_20260620.md",
     DOCS / "02_relatorio_completo.md"),
]

for origem, destino in copias_docs:
    if origem.exists():
        shutil.copy2(origem, destino)
        print(f"✅ {destino.name}")
    else:
        print(f"❌ Não encontrado: {origem}")

# ── Anexos ─────────────────────────────────────────────────────────────
copias_anexos = [
    # Pregão 00030/2026 — café + asfalto
    (RAW / "transparencia_ferraz/casamax/xlsx-compras-licitacoes/4270.xlsx",
     ANEXOS / "01_pregao_00030_2026_cafe_e_asfalto.xlsx"),

    # SINAPI — preços CBUQ
    (PROCESSED / "sinapi/sinapi_cbuq_precos.csv",
     ANEXOS / "02_sinapi_precos_cbuq_referencia.csv"),

    # DATACITY — contratos e aditivos
    (PROCESSED / "transparencia_ferraz/datacity_contratos_template.xlsx",
     ANEXOS / "03_datacity_contratos_e_aditivos.xlsx"),

    # CASAMAX — itens por processo
    (PROCESSED / "transparencia_ferraz/casamax_compras_itens.csv",
     ANEXOS / "04_casamax_itens_por_processo.csv"),

    # Emendas federais
    (PROCESSED / "portal_federal/emendas_federais_ferraz.csv",
     ANEXOS / "05_emendas_federais_ferraz_2020_2024.csv"),

    # CASAMAX — contratos portal
    (PROCESSED / "transparencia_ferraz/casamax_contratos.csv",
     ANEXOS / "06_casamax_contratos_portal_municipal.csv"),

    # DATACITY — contratos portal
    (PROCESSED / "transparencia_ferraz/datacity_contratos.csv",
     ANEXOS / "07_datacity_contratos_portal_municipal.csv"),

    # Fracionamento
    (PROCESSED / "tce_sp/suspeitos_fracionamento.csv",
     ANEXOS / "08_fracionamento_despesa.csv"),

    # Locações
    (PROCESSED / "tce_sp/locacoes_imoveis.csv",
     ANEXOS / "09_locacoes_imoveis_suspeitas.csv"),
]

print()
for origem, destino in copias_anexos:
    if origem.exists():
        shutil.copy2(origem, destino)
        print(f"✅ {destino.name}")
    else:
        print(f"❌ Não encontrado: {origem.relative_to(Path('.'))}")

# ── PDFs DATACITY ──────────────────────────────────────────────────────
print()
pdf_dir_destino = ANEXOS / "10_pdfs_contratos_datacity"
pdf_dir_destino.mkdir(exist_ok=True)
pdf_origem = RAW / "transparencia_ferraz/datacity/pdfs-complementares"

count = 0
for pdf in pdf_origem.rglob("*.pdf"):
    shutil.copy2(pdf, pdf_dir_destino / pdf.name)
    count += 1
print(f"✅ {count} PDFs DATACITY copiados → {pdf_dir_destino.name}/")

# ── Resumo final ───────────────────────────────────────────────────────
print()
print("=" * 55)
print("PASTA DE DENÚNCIA PREPARADA")
print("=" * 55)
print(f"\nLocalização: {BASE.resolve()}")
print(f"\nDocumentos:")
for f in sorted(DOCS.iterdir()):
    print(f"  {f.name} — {f.stat().st_size/1e3:.0f} KB")
print(f"\nAnexos:")
for f in sorted(ANEXOS.iterdir()):
    if f.is_file():
        print(f"  {f.name} — {f.stat().st_size/1e3:.0f} KB")
    else:
        pdfs = list(f.rglob("*.pdf"))
        print(f"  {f.name}/ — {len(pdfs)} PDFs")
print(f"\n✅ Tudo pronto para a denúncia ao TCE-SP!")
print(f"   Canal: https://www.tce.sp.gov.br/fale-conosco")