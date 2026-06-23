import openpyxl
import pandas as pd
from pathlib import Path

CASAMAX_DIR = Path("data/raw/transparencia_ferraz/casamax/xlsx-compras-licitacoes")
DATACITY_DIR = Path("data/raw/transparencia_ferraz/datacity/xlsx-compras-licitacoes")
PROCESSED_DIR = Path("data/processed/transparencia_ferraz")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def ler_xlsx_compras(caminho: Path) -> pd.DataFrame:
    """Lê arquivo de compras por itens do portal de Ferraz."""
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))

    # Extrai metadados do cabeçalho
    processo = ""
    for row in rows[:8]:
        if len(row) > 2 and row[1] and "Número" in str(row[1]):
            processo = str(row[2]).strip()
            break

    # Encontra a linha de cabeçalho
    header_idx = None
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0] and "Descrição" in str(row[0]):
            header_idx = i
            break

    if header_idx is None:
        wb.close()
        return pd.DataFrame()

    # Extrai dados
    registros = []
    for row in rows[header_idx + 1:]:
        if len(row) < 5 or not row[0]:
            continue
        desc = str(row[0]).strip()[:100]
        unidade = str(row[1]).strip() if len(row) > 1 and row[1] else ""
        qtd = row[2] if len(row) > 2 else None
        vl_unit = row[3] if len(row) > 3 else None
        vl_total = row[4] if len(row) > 4 else None
        vencedor = str(row[5]).strip() if len(row) > 5 and row[5] else ""

        cnpj_venc = ""
        if "(" in vencedor and ")" in vencedor:
            cnpj_venc = vencedor.split("(")[-1].replace(")", "").strip()
            vencedor = vencedor.split("(")[0].strip()

        registros.append({
            "processo": processo,
            "arquivo": caminho.name,
            "descricao": desc,
            "unidade": unidade,
            "quantidade": qtd,
            "valor_unitario": vl_unit,
            "valor_total": vl_total,
            "vencedor": vencedor,
            "cnpj_vencedor": cnpj_venc,
        })

    wb.close()
    return pd.DataFrame(registros)

# ── Processa CASAMAX ──────────────────────────────────────────────────
print("=" * 70)
print("CASAMAX — COMPRAS POR ITENS")
print("=" * 70)

frames_casamax = []
for xlsx in sorted(CASAMAX_DIR.glob("*.xlsx")):
    df = ler_xlsx_compras(xlsx)
    if not df.empty:
        frames_casamax.append(df)
        print(f"\n📄 {xlsx.name} — Processo {df['processo'].iloc[0]}")
        print(f"   {len(df)} itens")

if frames_casamax:
    casamax_itens = pd.concat(frames_casamax, ignore_index=True)
    casamax_itens["valor_total"] = pd.to_numeric(casamax_itens["valor_total"], errors="coerce")
    casamax_itens["valor_unitario"] = pd.to_numeric(casamax_itens["valor_unitario"], errors="coerce")

    # Filtra só itens vencidos pela CASAMAX
    casamax_ganhou = casamax_itens[
        casamax_itens["cnpj_vencedor"].str.replace(r"[.\-/]", "", regex=True).str.strip() == "08183516000120"
    ]

    print(f"\n{'='*70}")
    print(f"Total de itens analisados: {len(casamax_itens)}")
    print(f"Itens vencidos pela CASAMAX: {len(casamax_ganhou)}")
    print(f"Valor total CASAMAX: R$ {casamax_ganhou['valor_total'].sum():,.2f}")

    print(f"\nItens CASAMAX por processo:")
    for processo, grupo in casamax_ganhou.groupby("processo"):
        print(f"\n  Processo {processo}:")
        for _, r in grupo.iterrows():
            print(f"    {r['descricao'][:60]}")
            print(f"    {r['quantidade']} {r['unidade']} × R$ {r['valor_unitario']:,.2f} = R$ {r['valor_total']:,.2f}")

    casamax_itens.to_csv(
        PROCESSED_DIR / "casamax_compras_itens.csv",
        index=False, encoding="utf-8-sig", sep=";"
    )

# ── Processa DATACITY ─────────────────────────────────────────────────
print(f"\n{'='*70}")
print("DATACITY — COMPRAS POR ITENS")
print("=" * 70)

frames_datacity = []
for xlsx in sorted(DATACITY_DIR.glob("*.xlsx")):
    df = ler_xlsx_compras(xlsx)
    if not df.empty:
        frames_datacity.append(df)
        print(f"\n📄 {xlsx.name} — Processo {df['processo'].iloc[0]}")
        print(f"   {len(df)} itens")

if frames_datacity:
    datacity_itens = pd.concat(frames_datacity, ignore_index=True)
    datacity_itens["valor_total"] = pd.to_numeric(datacity_itens["valor_total"], errors="coerce")
    datacity_itens["valor_unitario"] = pd.to_numeric(datacity_itens["valor_unitario"], errors="coerce")

    datacity_ganhou = datacity_itens[
        datacity_itens["cnpj_vencedor"].str.replace(r"[.\-/]", "", regex=True).str.strip() == "02679522000197"
    ]

    print(f"\nTotal de itens analisados: {len(datacity_itens)}")
    print(f"Itens vencidos pela DATACITY: {len(datacity_ganhou)}")
    print(f"Valor total DATACITY: R$ {datacity_ganhou['valor_total'].sum():,.2f}")

    print(f"\nItens DATACITY por processo:")
    for processo, grupo in datacity_ganhou.groupby("processo"):
        print(f"\n  Processo {processo}:")
        for _, r in grupo.iterrows():
            print(f"    {r['descricao'][:60]}")
            print(f"    {r['quantidade']} {r['unidade']} × R$ {r['valor_unitario']:,.2f} = R$ {r['valor_total']:,.2f}")

    datacity_itens.to_csv(
        PROCESSED_DIR / "datacity_compras_itens.csv",
        index=False, encoding="utf-8-sig", sep=";"
    )

print(f"\nArquivos salvos em: {PROCESSED_DIR}")