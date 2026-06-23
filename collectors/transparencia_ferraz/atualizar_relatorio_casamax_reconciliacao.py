from pathlib import Path

DOCS_DIR = Path("docs")

relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

adicao = """

### 9.5 CASAMAX — Reconciliação entre Portal Municipal e TCE-SP

| Fonte | Valor Total | Período |
|---|---|---|
| TCE-SP (empenhos) | R$ 87.500.497,17 | 2020–2025 |
| Portal Municipal (contratos) | R$ 42.815.257,30 | contratos vigentes |
| **Diferença** | **R$ 44.684.239,87** | — |

**Explicação do gap:** o Portal da Transparência Municipal exibe apenas
contratos vigentes ou recentes, enquanto o TCE-SP registra todos os
empenhos históricos. A diferença não configura irregularidade — é uma
limitação do portal municipal.

**Composição dos gastos por elemento de despesa (TCE-SP 2020–2025):**

| Elemento | Valor | % |
|---|---|---|
| Obras em andamento | R$ 62.110.212,73 | 71% |
| Outros materiais de consumo | R$ 15.687.625,84 | 18% |
| Obras e instalações | R$ 8.457.251,85 | 10% |
| Outros serviços de terceiros | R$ 1.008.000,00 | 1% |

**Evolução anual dos empenhos:**

| Ano | Valor Empenhado |
|---|---|
| 2020 | R$ 4.452.672,40 |
| 2021 | R$ 4.766.256,06 |
| 2022 | R$ 34.520.040,70 |
| 2023 | R$ 32.049.640,77 |
| 2024 | R$ 7.610.331,31 |
| 2025 | R$ 4.101.555,93 |

O pico de **R$ 66,5 milhões em 2022-2023** coincide com os contratos de
recapeamento e pavimentação identificados nos ajustes do TCE-SP.
A queda expressiva em 2024-2025 sugere encerramento dos grandes contratos
de obras, com apenas manutenção e fornecimento de materiais remanescentes.

**Conclusão:** a CASAMAX atua essencialmente como empreiteira de obras
(71% dos gastos em "Obras em andamento"). Os valores são expressivos mas
compatíveis com obras de pavimentação em larga escala. A investigação
pendente (P013) foca na classificação indevida do concreto usinado como
"material de consumo" e na necessidade de comparação de preços com o SINAPI.
"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    adicao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print(f"Relatório atualizado: {relatorio.name}")