import xlrd
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw/sinapi/nao-desonerado")
PROCESSED_DIR = Path("data/processed/sinapi")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

ARQUIVOS = {
    "jun-22": RAW_DIR / "jun-22/SINAPI_Preco_Ref_Insumos_SP_062022_NaoDesonerado.XLS",
    "dez-22": RAW_DIR / "dez-22/SINAPI_Preco_Ref_Insumos_SP_122022_NaoDesonerado.XLS",
    "jun-23": RAW_DIR / "jun-23/SINAPI_Preco_Ref_Insumos_SP_062023_NaoDesonerado.XLS",
    "dez-23": RAW_DIR / "dez-23/SINAPI_Preco_Ref_Insumos_SP_202312_NaoDesonerado.xlsx",
}

TERMOS_CBUQ = ["CBUQ", "BETUMINOSO", "CONCRETO ASFALTICO"]

def buscar_precos(caminho: Path, periodo: str) -> list:
    resultados = []
    try:
        ext = caminho.suffix.lower()
        if ext == ".xls":
            wb = xlrd.open_workbook(caminho)
            ws = wb.sheet_by_index(0)
            rows = [ws.row_values(i) for i in range(ws.nrows)]
        elif ext == ".xlsx":
            import openpyxl
            wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
            ws = wb.active
            rows = [list(row) for row in ws.iter_rows(values_only=True)]
        else:
            return []

        for row in rows:
            if len(row) < 5:
                continue
            desc = str(row[1]).upper()
            if any(t in desc for t in TERMOS_CBUQ):
                try:
                    preco = float(str(row[4]).replace(".", "").replace(",", "."))
                except:
                    continue
                resultados.append({
                    "periodo":    periodo,
                    "codigo":     row[0],
                    "descricao":  str(row[1]).strip(),
                    "unidade":    str(row[2]).strip(),
                    "preco_sinapi": preco,
                })
    except Exception as e:
        print(f"Erro em {periodo}: {e}")
    return resultados
# Coleta preços de todos os períodos
todos = []
for periodo, caminho in ARQUIVOS.items():
    if caminho.exists():
        dados = buscar_precos(caminho, periodo)
        todos.extend(dados)
        print(f"{periodo}: {len(dados)} insumos encontrados")
    else:
        # Tenta encontrar o arquivo com nome diferente
        pasta = caminho.parent
        xls = list(pasta.glob("SINAPI_Preco*.XLS")) + list(pasta.glob("SINAPI_Preco*.xls"))
        if xls:
            dados = buscar_precos(xls[0], periodo)
            todos.extend(dados)
            print(f"{periodo}: {len(dados)} insumos encontrados ({xls[0].name})")
        else:
            print(f"{periodo}: arquivo não encontrado em {pasta}")

df = pd.DataFrame(todos)

if df.empty:
    print("Nenhum dado coletado!")
else:
    # Filtra apenas CBUQ relevantes
    cbuq = df[df["descricao"].str.contains("CBUQ|BETUMINOSO USINADO", na=False)].copy()

    print("\n" + "=" * 70)
    print("PREÇOS SINAPI — CBUQ — SÃO PAULO")
    print("=" * 70)

    for _, row in cbuq.iterrows():
        print(f"\n{row['periodo']} | {row['descricao'][:80]}")
        print(f"  Unidade: {row['unidade']} | Preço SINAPI: R$ {row['preco_sinapi']:,.2f}")

    # Contratos CASAMAX de concreto usinado (dados dos ajustes)
    print("\n" + "=" * 70)
    print("CONTRATOS CASAMAX — CONCRETO USINADO")
    print("=" * 70)

    casamax_contratos = [
        {"periodo": "jun-22", "descricao": "Aquisição de Concreto Usinado", "valor_total": 699541.50},
        {"periodo": "dez-22", "descricao": "Aquisição de Concreto Usinado", "valor_total": 2139774.00},
        {"periodo": "dez-22", "descricao": "Aquisição de Concreto Usinado", "valor_total": 1329951.84},
        {"periodo": "dez-22", "descricao": "Aquisição de Concreto Usinado", "valor_total": 799946.28},
        {"periodo": "dez-22", "descricao": "Aquisição de Concreto Usinado", "valor_total": 479528.84},
        {"periodo": "jun-23", "descricao": "Aquisição de Concreto Usinado", "valor_total": 1499723.00},
        {"periodo": "dez-23", "descricao": "Aquisição de Concreto Usinado", "valor_total": 27965.00},
        {"periodo": "jun-23", "descricao": "Aquisição de Concreto Usinado", "valor_total": 2207637.00},
    ]

    df_casamax = pd.DataFrame(casamax_contratos)
    print(f"\nTotal pago em concreto usinado: R$ {df_casamax['valor_total'].sum():,.2f}")

    # Salva
    cbuq.to_csv(PROCESSED_DIR / "sinapi_cbuq_precos.csv", index=False, encoding="utf-8-sig", sep=";")
    df_casamax.to_csv(PROCESSED_DIR / "casamax_contratos_concreto.csv", index=False, encoding="utf-8-sig", sep=";")
    print(f"\nArquivos salvos em: {PROCESSED_DIR}")

    # Adicione ao final do analisar_precos_casamax.py

print("\n" + "=" * 70)
print("ANÁLISE COMPARATIVA — CASAMAX vs SINAPI")
print("=" * 70)

# Preços SINAPI médios por período (CAP 30/45 - mais comum)
sinapi_medio = {
    "jun-22": 500.25,
    "dez-22": 513.98,
    "jun-23": 490.44,
    "dez-23": 502.70,
}

# Contratos com período aproximado
analise = [
    {"periodo": "jun-22", "valor": 699541.50,   "descricao": "1º semestre 2022"},
    {"periodo": "dez-22", "valor": 2139774.00,  "descricao": "2º semestre 2022 (A)"},
    {"periodo": "dez-22", "valor": 1329951.84,  "descricao": "2º semestre 2022 (B)"},
    {"periodo": "dez-22", "valor": 799946.28,   "descricao": "2º semestre 2022 (C)"},
    {"periodo": "dez-22", "valor": 479528.84,   "descricao": "2º semestre 2022 (D)"},
    {"periodo": "jun-23", "valor": 1499723.00,  "descricao": "1º semestre 2023"},
    {"periodo": "jun-23", "valor": 2207637.00,  "descricao": "2º semestre 2023 (A)"},
    {"periodo": "dez-23", "valor": 27965.00,    "descricao": "2º semestre 2023 (B)"},
]

print(f"\n{'Contrato':<30} {'Valor Pago':>14} {'Ton. estimadas':>15} {'Preço/ton implícito':>20} {'Preço SINAPI':>13} {'Diferença':>12}")
print("-" * 110)

total_pago = 0
total_sinapi = 0

for item in analise:
    preco_ref = sinapi_medio[item["periodo"]]
    ton_estimadas = item["valor"] / preco_ref
    preco_implicito = item["valor"] / ton_estimadas  # = preco_ref, mas útil para visualizar
    valor_sinapi = ton_estimadas * preco_ref
    diferenca = item["valor"] - valor_sinapi

    total_pago += item["valor"]
    total_sinapi += valor_sinapi

    print(f"{item['descricao']:<30} R$ {item['valor']:>12,.2f} {ton_estimadas:>14.0f}t "
          f"R$ {preco_implicito:>17,.2f}/t  R$ {preco_ref:>10,.2f}/t  R$ {diferenca:>10,.2f}")

print("-" * 110)
print(f"\n⚠️  Nota: sem a quantidade real em toneladas dos contratos, não é possível")
print(f"    calcular superfaturamento preciso. A análise acima usa preço SINAPI como")
print(f"    referência para estimar tonelagem — os valores implícitos batem com SINAPI")
print(f"    pois foram calculados a partir dele.")
print(f"\n✅ Recomendação: solicitar via LAI as notas fiscais da CASAMAX com")
print(f"    quantidade em toneladas para comparação direta com SINAPI.")
print(f"\nTotal pago: R$ {total_pago:,.2f}")
print(f"Referência SINAPI: R$ {total_sinapi:,.2f}")