from pathlib import Path

DOCS_DIR = Path("docs")
relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

adicao = """

### 9.7 CASAMAX — Análise de preços por processo licitatório

Análise dos itens vencidos pela CASAMAX em 4 processos licitatórios,
todos classificados como "material de consumo":

| Processo | Produto | Qtd (t) | Preço/t | Total | vs SINAPI* |
|---|---|---|---|---|---|
| 00032 (11697) | CBUQ Faixa III e IV | 14.000 | R$ 498,00 | R$ 6.972.000 | ✅ dentro |
| 00059 (13846) | CBUQ Faixa III e IV | 11.200 | R$ 548,66 | R$ 6.144.992 | ⚠️ +9% |
| 00030 (4270) | Concreto Asfáltico Faixa IV e V | 16.000 | R$ 640–648 | R$ 10.304.000 | 🔴 +28% |
| 00030 (4270) | Material Betuminoso Reciclado | 5.000 | R$ 290,00 | R$ 1.450.000 | — |

*SINAPI SP jun/2022: R$ 500,25/t para CBUQ Faixa C CAP 30/45

**Total CASAMAX nos 4 processos: R$ 24.870.992,00**

**Observações:**

1. **Escalada de preços** — o preço do CBUQ saltou de R$ 498/t (processo 00032)
   para R$ 648/t (processo 00030), um aumento de **30%** entre os processos.
   O processo 00030 é o mais recente (2026) e apresenta o maior desvio em
   relação ao SINAPI.

2. **Classificação indevida confirmada em todos os processos** — concreto
   asfáltico licitado como "material de consumo" em todos os casos analisados,
   independentemente do volume (até 16.000 toneladas em um único processo).

3. **Concentração em único fornecedor** — a CASAMAX venceu 100% dos lotes
   de material asfáltico em todos os processos analisados.

### 9.8 DATACITY — Itens por processo licitatório

| Processo | Objeto | Qtd | Valor |
|---|---|---|---|
| 00038 (7609) | Prestação de serviços — radares | 1 UN | R$ 3.540.000,00 |
| 00034 (7102) | Prestação de serviços — apoio técnico (6 itens) | 1 UN cada | R$ 1.164.000,00 |

Serviços contratados por "unidade" sem discriminação de horas,
equipamentos ou métricas de entrega — prática que dificulta
a auditoria da execução contratual.
"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    adicao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print("Relatório atualizado!")
print("Achados documentados: escalada de preços CASAMAX, DATACITY sem métricas")