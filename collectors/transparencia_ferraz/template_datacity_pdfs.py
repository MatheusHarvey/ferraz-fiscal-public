import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed/transparencia_ferraz")

# Template com os 12 PDFs organizados para preenchimento manual
dados = [
    # SIAM 111/2021 — Luminárias
    {"siam": "111/2021", "tipo": "Contrato Original", "arquivo": "contrato 1112021.pdf",
     "objeto": "Fornecimento e instalação de luminárias públicas",
     "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},

    # SIAM 189/2021 — Apoio técnico
    {"siam": "189/2021", "tipo": "Contrato Original", "arquivo": "ctt1892021.pdf",
     "objeto": "Serviço de apoio técnico tecnológico manutenção preventiva e corretiva de rede",
     "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},
    {"siam": "189/2021", "tipo": "1º Aditivo", "arquivo": "1 adt contr 1892021.pdf",
     "objeto": "", "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},
    {"siam": "189/2021", "tipo": "3º Aditivo", "arquivo": "3 adt contr 1892021.pdf",
     "objeto": "", "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},
    {"siam": "189/2021", "tipo": "4º Aditivo", "arquivo": "4__adt_contrato_n__1892021.pdf",
     "objeto": "", "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},
    {"siam": "189/2021", "tipo": "5º Aditivo", "arquivo": "5__adt_contrago_189_2021_datacity.pdf",
     "objeto": "", "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},

    # SIAM 243/2020 — Luminárias
    {"siam": "243/2020", "tipo": "Contrato Original", "arquivo": "contrato2432020.pdf",
     "objeto": "Fornecimento e instalação de luminárias públicas",
     "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},
    {"siam": "243/2020", "tipo": "1º Aditivo", "arquivo": "1-adt 2432020.pdf",
     "objeto": "", "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},

    # SIAM 329/2022 — Radares
    {"siam": "329/2022", "tipo": "Contrato Original", "arquivo": "contrato 3292022.pdf",
     "objeto": "Monitoramento e fiscalização de tráfego de veículos",
     "valor_original": "", "vigencia_inicio": "31/08/2022", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": "Pregão 038/2021"},
    {"siam": "329/2022", "tipo": "1º Aditivo", "arquivo": "1 adt cont 3292022.pdf",
     "objeto": "", "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": ""},
    {"siam": "329/2022", "tipo": "2º Aditivo", "arquivo": "2__adt_contrato_329_2022_datacity.pdf",
     "objeto": "Prorrogação 12 meses", "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "28/08/2024",
     "num_aditivos": "", "observacoes": "Texto extraível — assinado 28/08/2024"},
    {"siam": "329/2022", "tipo": "3º Aditivo", "arquivo": "3__adt_contrato_329_2022_datacity.pdf",
     "objeto": "", "valor_original": "", "vigencia_inicio": "", "vigencia_fim": "",
     "num_aditivos": "", "observacoes": "Texto extraível"},
]

df = pd.DataFrame(dados)

# Salva como Excel para facilitar preenchimento
saida = PROCESSED_DIR / "datacity_contratos_template.xlsx"
df.to_excel(saida, index=False)
print(f"Template salvo em: {saida}")
print(f"Total de linhas: {len(df)}")
print(f"\nColunas para preencher:")
print("  - valor_original: valor do contrato/aditivo em R$")
print("  - vigencia_inicio: data de início (dd/mm/aaaa)")
print("  - vigencia_fim: data de término (dd/mm/aaaa)")
print("  - num_aditivos: número de aditivos se for contrato original")
print("  - observacoes: qualquer informação relevante")