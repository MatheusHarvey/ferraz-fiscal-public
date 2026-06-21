from pathlib import Path
from datetime import date

DOCS_DIR = Path("../../docs")

# Adiciona nota ao relatório existente
relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

nota = """
---

## 8. Achados sem irregularidade

### 8.1 Dispensas de medicamentos — gestão adequada

A análise das 607 dispensas de medicamentos identificadas entre 2020 e 2024 não revelou
indícios de irregularidade. Pelo contrário, o volume elevado em 2024 (+972% em relação
à média histórica) decorreu da consolidação de compras em poucos processos:

- **Março/2024:** 208 itens distribuídos em apenas 2 processos licitatórios
- **Dezembro/2024:** 206 itens em 1 único processo

Esse padrão indica reposição semestral consolidada de estoque da farmácia municipal,
prática tecnicamente correta e mais eficiente do que múltiplas compras fracionadas.
Os medicamentos identificados são de uso crônico essencial (hipertensão, diabetes,
colesterol, asma), compatíveis com um programa de distribuição à população.

**Avaliação:** ponto positivo da gestão atual.

---

*Relatório atualizado em {}*
""".format(date.today().strftime("%d/%m/%Y"))

# Substitui rodapé e adiciona seção
conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    nota + "\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print(f"Relatório atualizado: {relatorio.name}")