from pathlib import Path

DOCS_DIR = Path("docs")
relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

adicao = """

### 9.9 CASAMAX — Consolidação final de valores

| Fonte | Valor | Observação |
|---|---|---|
| TCE-SP — empenhos 2020–2025 | R$ 87.500.497,17 | Total histórico completo |
| Portal Municipal — contratos vigentes | R$ 42.815.257,30 | Apenas contratos ativos |
| Itens identificados nos processos | R$ 24.870.992,00 | 4 processos analisados |

**Composição dos R$ 87,5 milhões (TCE-SP):**

| Elemento de despesa | Valor | % |
|---|---|---|
| Obras em andamento | R$ 62.110.212,73 | 71% |
| Outros materiais de consumo (CBUQ) | R$ 15.687.625,84 | 18% |
| Obras e instalações | R$ 8.457.251,85 | 10% |
| Outros | R$ 1.244.406,75 | 1% |

**Gap entre fontes:** R$ 44,6 milhões — explicado pelo portal municipal
exibir apenas contratos vigentes, enquanto o TCE-SP registra
todos os empenhos históricos desde 2020.

**Resumo dos achados CASAMAX:**

1. R$ 87,5 milhões empenhados em 2020–2025 — maior fornecedor de obras
2. Pico de R$ 66,5 milhões em 2022–2023 — obras de recapeamento
3. R$ 15,7 milhões em concreto usinado classificado como "material de consumo"
4. Escalada de preços: R$ 498/t → R$ 548/t → R$ 648/t (+30%)
5. Pregão 00030/2026 — concreto asfáltico licitado junto com café e biscoitos
6. Preço 2026 (R$ 640–648/t) 28% acima do SINAPI (R$ 500/t)
7. 100% dos lotes de material asfáltico vencidos pela CASAMAX
"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    adicao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print("Relatório atualizado com consolidação final CASAMAX!")