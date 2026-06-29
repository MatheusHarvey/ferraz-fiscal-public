import fitz
import re
import pandas as pd
from pathlib import Path

PDF_DIR = Path("data/raw/transparencia_ferraz/datacity/pdfs-complementares")
PROCESSED_DIR = Path("data/processed/transparencia_ferraz")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def extrair_texto(caminho: Path) -> str:
    doc = fitz.open(caminho)
    texto = ""
    for page in doc:
        t = page.get_text()
        if t.strip():
            texto += t + "\n"
    doc.close()
    return texto

def extrair_valor(texto: str) -> str:
    """Tenta extrair valor do contrato/aditivo."""
    padroes = [
        r"R\$\s*[\d\.,]+",
        r"valor\s+(?:global|total|mensal|do\s+contrato)[^\n]*[\d\.,]+",
        r"importância\s+de[^\n]*[\d\.,]+",
        r"R\$\s*\([\w\s]+\)",
    ]
    for p in padroes:
        matches = re.findall(p, texto, re.IGNORECASE)
        if matches:
            return " | ".join(matches[:5])
    return "não encontrado"

def identificar_tipo(nome: str) -> str:
    nome = nome.lower()
    if "adt" in nome or "aditamento" in nome or "aditivo" in nome:
        # Tenta pegar o número do aditivo
        m = re.search(r"(\d+)[_\s]*adt", nome)
        if m:
            return f"{m.group(1)}º Aditivo"
        return "Aditivo"
    if "contrato" in nome or "ctt" in nome:
        return "Contrato Original"
    return "Documento"

# Processa todos os PDFs
registros = []

for pasta in sorted(PDF_DIR.iterdir()):
    if not pasta.is_dir():
        continue
    siam = pasta.name
    print(f"\n{'='*60}")
    print(f"SIAM: {siam}")
    print(f"{'='*60}")

    for pdf in sorted(pasta.glob("*.pdf")):
        tipo = identificar_tipo(pdf.name)
        texto = extrair_texto(pdf)
        tem_texto = len(texto.strip()) > 100
        valor = extrair_valor(texto) if tem_texto else "PDF sem texto extraível"

        print(f"\n  📄 {pdf.name}")
        print(f"     Tipo: {tipo}")
        print(f"     Texto extraível: {'✅' if tem_texto else '❌'}")
        print(f"     Valores encontrados: {valor[:100]}")

        if tem_texto:
            # Mostra trecho relevante
            for linha in texto.split("\n"):
                if any(k in linha.lower() for k in [
                    "valor", "r$", "mensal", "global", "total",
                    "vigência", "vigencia", "prazo", "meses"
                ]):
                    print(f"     >> {linha.strip()[:120]}")

        registros.append({
            "siam": siam,
            "arquivo": pdf.name,
            "tipo": tipo,
            "tem_texto": tem_texto,
            "valores_extraidos": valor,
            "tamanho_kb": pdf.stat().st_size // 1000,
        })

# Salva resumo
df = pd.DataFrame(registros)
df.to_csv(PROCESSED_DIR / "datacity_pdfs_analise.csv",
          index=False, encoding="utf-8-sig", sep=";")

print(f"\n{'='*60}")
print(f"RESUMO")
print(f"{'='*60}")
print(f"Total de PDFs: {len(registros)}")
print(f"Com texto extraível: {df['tem_texto'].sum()}")
print(f"Sem texto: {(~df['tem_texto']).sum()}")
print(f"\nSalvo em: data/processed/transparencia_ferraz/datacity_pdfs_analise.csv")