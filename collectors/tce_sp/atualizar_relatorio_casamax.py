from pathlib import Path

DOCS_DIR = Path("docs")

relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

adicao = """

### 9.3 CASAMAX — Classificação indevida de insumo de obra

Além do volume expressivo de contratos, identificou-se que **R$ 9.184.067,46** em 
aquisições de **concreto usinado (CBUQ)** foram classificados como 
"Outros materiais de consumo" em vez de insumo de obra, distribuídos em 
**8 contratos separados** entre 2022 e 2024:

| Período | Valor | Descrição |
|---|---|---|
| 2022/1º sem | R$ 699.541,50 | Aquisição de Concreto Usinado |
| 2022/2º sem | R$ 2.139.774,00 | Aquisição de Concreto Usinado |
| 2022/2º sem | R$ 1.329.951,84 | Aquisição de Concreto Usinado |
| 2022/2º sem | R$ 799.946,28 | Aquisição de Concreto Usinado |
| 2022/2º sem | R$ 479.528,84 | Aquisição de Concreto Usinado |
| 2023/2º sem | R$ 1.499.723,00 | Aquisição de Concreto Usinado |
| 2023/2º sem | R$ 27.965,00 | Aquisição de Concreto Usinado |
| 2024/1º sem | R$ 2.207.637,00 | Aquisição de Concreto Usinado |

**Indício:** concreto usinado é insumo de obra, não material de consumo. 
A classificação incorreta pode ter permitido processos licitatórios menos rigorosos 
e dificulta a auditoria do custo real das obras. Os 8 contratos separados 
sugerem ainda possível fracionamento de despesa.

**Recomendação:** solicitar via LAI os processos licitatórios referentes a cada 
aquisição de concreto e verificar se os preços pagos são compatíveis com o 
mercado regional para CBUQ.
"""

# Insere após a seção 9.2
conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    adicao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print(f"Relatório atualizado: {relatorio.name}")