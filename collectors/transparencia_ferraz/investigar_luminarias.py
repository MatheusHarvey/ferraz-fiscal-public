from pathlib import Path
from datetime import date

DOCS_DIR = Path("docs")

print("=" * 60)
print("P017 — DATACITY LUMINÁRIAS — ANÁLISE DE SOBREPOSIÇÃO")
print("=" * 60)

contratos = [
    {
        "numero": "243/2020",
        "objeto": "Fornecimento e instalação de luminárias públicas LED",
        "valor": 1964132.00,
        "inicio": "04/11/2020",
        "fim": "03/08/2021",
        "processo": "G00028",
    },
    {
        "numero": "111/2021",
        "objeto": "Fornecimento e instalação de luminárias de LED",
        "valor": 1479545.04,
        "inicio": "23/06/2021",
        "fim": "22/06/2022",
        "processo": "G00028",
    },
]

print("\nContratos identificados:")
for c in contratos:
    print(f"\n  Contrato {c['numero']}")
    print(f"  Objeto:   {c['objeto']}")
    print(f"  Valor:    R$ {c['valor']:,.2f}")
    print(f"  Vigência: {c['inicio']} a {c['fim']}")
    print(f"  Processo: {c['processo']}")

print("\n" + "=" * 60)
print("ACHADOS:")
print("=" * 60)
print("""
1. SOBREPOSIÇÃO DE VIGÊNCIA: os contratos 243/2020 e 111/2021
   coexistiram entre 23/06/2021 e 03/08/2021 (aproximadamente 
   40 dias), período em que o município pagava dois contratos 
   simultâneos para o mesmo objeto e mesmo fornecedor.

2. OBJETO IDÊNTICO: ambos os contratos têm como objeto o 
   fornecimento e instalação de luminárias públicas LED nas 
   vias do município.

3. MESMO PROCESSO LICITATÓRIO (G00028): os dois contratos 
   derivam do mesmo processo administrativo, o que levanta 
   a questão de se tratar de um único contrato dividido ou 
   de um aditivo incorretamente registrado como novo contrato.

4. VALOR TOTAL: R$ 3.443.677,04 para luminárias em dois 
   contratos consecutivos para o mesmo fornecedor.
""")

# Atualiza pendencias.md
pendencias = Path("pendencias.md")
conteudo = pendencias.read_text(encoding="utf-8")

conteudo = conteudo.replace(
    "### [P017] Contratos de luminárias DATACITY — possível duplicidade",
    "### [P017] Contratos de luminárias DATACITY — RESOLVIDO ✅"
)

# Adiciona na tabela de resolvidas
conteudo = conteudo.replace(
    "| P008 | Dispensas de consultoria — 1 contrato FIA/USP R$ 397k, sem irregularidade | Sessão atual |",
    "| P008 | Dispensas de consultoria — 1 contrato FIA/USP R$ 397k, sem irregularidade | Sessão atual |\n| P017 | Luminárias DATACITY — sobreposição de 40 dias entre contratos 243/2020 e 111/2021 | Sessão atual |"
)

pendencias.write_text(conteudo, encoding="utf-8")
print("pendencias.md atualizado!")

# Adiciona ao relatório
relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo_rel = relatorio.read_text(encoding="utf-8")

adicao = """

### 5.6 Contratos de luminárias — sobreposição de vigência

Os contratos 243/2020 e 111/2021, ambos para fornecimento e
instalação de luminárias públicas LED, apresentam sobreposição
de vigência de aproximadamente 40 dias:

| Contrato | Vigência | Valor |
|---|---|---|
| 243/2020 | 04/11/2020 a 03/08/2021 | R$ 1.964.132,00 |
| 111/2021 | 23/06/2021 a 22/06/2022 | R$ 1.479.545,04 |
| **Total** | | **R$ 3.443.677,04** |

**Sobreposição:** 23/06/2021 a 03/08/2021 (~40 dias)

**Indícios:**
- Objeto idêntico para o mesmo fornecedor em contratos consecutivos
- Ambos derivam do mesmo processo administrativo (G00028)
- Município pagou dois contratos simultâneos para o mesmo serviço
- Possível divisão irregular de contrato ou aditivo registrado como novo contrato
"""

conteudo_rel = conteudo_rel.replace(
    "### 5.5 Indícios consolidados",
    adicao + "\n### 5.5 Indícios consolidados"
)

relatorio.write_text(conteudo_rel, encoding="utf-8")
print("Relatório atualizado com P017!")