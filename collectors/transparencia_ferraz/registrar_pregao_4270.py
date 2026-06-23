from pathlib import Path

DOCS_DIR = Path("docs")
relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

adicao = """

### 9.6 CASAMAX — Pregão Eletrônico 00030/2026 (Processo 4270)

**🔴 ACHADO CRÍTICO — Classificação indevida confirmada**

No Pregão Eletrônico nº 00030/2026, processo administrativo 4270,
identificou-se a mistura de insumos de obra com gêneros alimentícios
no mesmo instrumento licitatório, todos classificados como
"material de consumo":

| Item | Unidade | Quantidade | Preço Unit. | Total | Vencedor |
|---|---|---|---|---|---|
| Açúcar refinado 1kg | UN | 3.750 | R$ 4,00 | R$ 15.000,00 | Nutricionale |
| Biscoito cream cracker 200g | PCT | 1.013 | R$ 2,50 | R$ 2.532,50 | Nutricionale |
| Café torrado 500g | UN | 1.170 | R$ 17,68 | R$ 20.685,60 | Orion |
| **Concreto Asfáltico Faixa V** | **T** | **8.000** | **R$ 648,00** | **R$ 5.184.000,00** | **CASAMAX** |
| **Concreto Asfáltico Faixa IV** | **T** | **8.000** | **R$ 640,00** | **R$ 5.120.000,00** | **CASAMAX** |
| **Material Betuminoso Reciclado** | **T** | **5.000** | **R$ 290,00** | **R$ 1.450.000,00** | **CASAMAX** |

**Total CASAMAX neste único pregão: R$ 11.754.000,00**

**Indícios identificados:**

1. **Classificação indevida confirmada** — Concreto asfáltico (insumo de obra)
   licitado no mesmo pregão que café, açúcar e biscoitos, todos sob a
   categoria "material de consumo". Insumos de obra devem ser licitados
   como obras ou serviços de engenharia, com critérios técnicos mais rigorosos.

2. **Preço acima do SINAPI** — O preço praticado de R$ 640–648/t para
   Concreto Asfáltico é aproximadamente **28% acima da referência SINAPI**
   para SP (R$ 500,25/t em jun/2022). Mesmo considerando atualização monetária
   pelo INCC de 2022 a 2026 (~20%), o valor permanece acima da referência.

3. **Volume expressivo** — 21.000 toneladas de material asfáltico em um
   único pregão (16.000t de CBUQ + 5.000t de material betuminoso reciclado),
   valor total de R$ 11,754 milhões, contratado como "material de consumo".

4. **Secretaria Municipal de Serviços Urbanos** — responsável por 21.000
   unidades do processo, o que confirma destinação para obras viárias.

**Recomendação:** este pregão constitui o indício mais claro de classificação
orçamentária indevida identificado na investigação. Recomenda-se incluir
na denúncia ao TCE-SP como exemplo concreto de irregularidade.
"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    adicao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print("Relatório atualizado com o Pregão 00030/2026!")
print("Total CASAMAX documentado: R$ 11.754.000,00")
print("Preço praticado: R$ 640-648/t vs SINAPI R$ 500/t (+28%)")