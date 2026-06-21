from pypdf import PdfReader
from pathlib import Path
import re

PDF_DIR = Path("../../data/raw/comprovante-cnpj")
PROCESSED_DIR = Path("../../data/processed/tce_sp")

def extrair_texto(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() or ""
    return texto

def extrair_campos(texto: str, cnpj: str) -> dict:
    """Extrai campos relevantes do comprovante da Receita Federal."""
    campos = {"cnpj": cnpj}

    # Razão social
    match = re.search(r"NOME EMPRESARIAL\s*[:\n]+\s*(.+)", texto, re.IGNORECASE)
    if not match:
        match = re.search(r"Razão Social[:\s]+(.+)", texto, re.IGNORECASE)
    campos["razao_social"] = match.group(1).strip() if match else ""

    # Situação cadastral
    match = re.search(r"SITUAÇÃO CADASTRAL\s*[:\n]+\s*(.+)", texto, re.IGNORECASE)
    if not match:
        match = re.search(r"Situação Cadastral[:\s]+(.+)", texto, re.IGNORECASE)
    campos["situacao"] = match.group(1).strip() if match else ""

    # Data da situação
    match = re.search(r"DATA DA SITUAÇÃO CADASTRAL\s*[:\n]+\s*(.+)", texto, re.IGNORECASE)
    if not match:
        match = re.search(r"Data da Situação[:\s]+(.+)", texto, re.IGNORECASE)
    campos["data_situacao"] = match.group(1).strip() if match else ""

    # Município
    match = re.search(r"MUNICÍPIO\s*[:\n]+\s*(.+)", texto, re.IGNORECASE)
    if not match:
        match = re.search(r"Município[:\s]+(.+)", texto, re.IGNORECASE)
    campos["municipio"] = match.group(1).strip() if match else ""

    # UF
    match = re.search(r"\bUF\b\s*[:\n]+\s*(.{2})", texto, re.IGNORECASE)
    campos["uf"] = match.group(1).strip() if match else ""

    # Data de abertura
    match = re.search(r"DATA DE ABERTURA\s*[:\n]+\s*(.+)", texto, re.IGNORECASE)
    if not match:
        match = re.search(r"Data de Abertura[:\s]+(.+)", texto, re.IGNORECASE)
    campos["data_abertura"] = match.group(1).strip() if match else ""

    # Atividade principal
    match = re.search(r"ATIVIDADE ECONÔMICA PRINCIPAL\s*[:\n]+\s*(.+)", texto, re.IGNORECASE)
    if not match:
        match = re.search(r"Atividade Principal[:\s]+(.+)", texto, re.IGNORECASE)
    campos["atividade"] = match.group(1).strip() if match else ""

    return campos

def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    print(f"PDFs encontrados: {len(pdfs)}\n")

    resultados = []

    for pdf_path in pdfs:
        cnpj = pdf_path.stem  # nome do arquivo sem extensão
        print(f"Lendo: {cnpj}")

        texto = extrair_texto(pdf_path)

        if not texto.strip():
            print(f"  ⚠ Sem texto extraível — pode ser PDF escaneado")
            resultados.append({"cnpj": cnpj, "situacao": "não lido"})
            continue

        campos = extrair_campos(texto, cnpj)
        resultados.append(campos)

        print(f"  Razão Social: {campos.get('razao_social', '')}")
        print(f"  Situação:     {campos.get('situacao', '')} ({campos.get('data_situacao', '')})")
        print(f"  Município:    {campos.get('municipio', '')} — {campos.get('uf', '')}")
        print(f"  Abertura:     {campos.get('data_abertura', '')}")
        print()

    # Salva resultado
    import pandas as pd
    df = pd.DataFrame(resultados)
    saida = PROCESSED_DIR / "cnpjs_enriquecidos.csv"
    df.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
    print(f"Salvo em: {saida}")

if __name__ == "__main__":
    main()