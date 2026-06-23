from pathlib import Path
from datetime import date
import pandas as pd

PROCESSED_DIR = Path("data/processed/transparencia_ferraz")
DOCS_DIR = Path("docs")

emendas = pd.read_csv(
    PROCESSED_DIR / "emendas_parlamentares.csv",
    sep=";", encoding="utf-8-sig"
)

for col in ["Orçado", "Empenhado", "Receita Recebida"]:
    emendas[col] = pd.to_numeric(emendas[col], errors="coerce")

# Top parlamentares
top_parl = emendas.groupby("Destinação")["Orçado"].sum().sort_values(ascending=False).head(10)

# Emendas suspeitas (receita > orçado)
suspeitas = emendas[emendas["Receita Recebida"] > emendas["Orçado"]].copy()
suspeitas_valor = suspeitas["Receita Recebida"].sum()

# Não empenhadas
nao_emp = emendas[(emendas["Orçado"] > 0) & (emendas["Empenhado"] == 0)]

relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

nova_secao = f"""
---

## 11. Emendas Parlamentares Municipais — 2026

Fonte: Portal da Transparência Municipal de Ferraz de Vasconcelos

### 11.1 Visão geral

| Indicador | Valor |
|---|---|
| Total de emendas | {len(emendas)} |
| Valor total orçado | R$ {emendas['Orçado'].sum():,.2f} |
| Valor total empenhado | R$ {emendas['Empenhado'].sum():,.2f} |
| Receita total recebida | R$ {emendas['Receita Recebida'].sum():,.2f} |
| Emendas sem empenhamento | {len(nao_emp)} (R$ {nao_emp['Orçado'].sum():,.2f}) |

### 11.2 Top 10 vereadores por valor orçado

| Vereador | Valor Orçado |
|---|---|
{"".join(f"| {parl} | R$ {valor:,.2f} |{chr(10)}" for parl, valor in top_parl.items())}

### 11.3 Emendas com receita recebida maior que o orçado

Foram identificadas **{len(suspeitas)} emendas** onde o valor recebido supera
o valor orçado, totalizando **R$ {suspeitas_valor:,.2f}** em recursos recebidos
acima do planejamento orçamentário. Isso pode indicar transferências federais
não previstas na LOA ou reclassificações orçamentárias.

| Emenda | Orçado | Recebido | Descrição |
|---|---|---|---|
{"".join(f"| {r['Nro Emenda']} | R$ {r['Orçado']:,.2f} | R$ {r['Receita Recebida']:,.2f} | {str(r['Descrição'])[:60]} |{chr(10)}" for _, r in suspeitas.iterrows())}

### 11.4 Emendas orçadas mas não empenhadas

**{len(nao_emp)} emendas** com valor total de **R$ {nao_emp['Orçado'].sum():,.2f}**
foram orçadas mas não tiveram execução registrada. Pode indicar emendas
aprovadas mas não executadas ou com execução pendente de registro.

"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    nova_secao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print(f"Relatório atualizado: {relatorio.name}")
print(f"Total de emendas documentadas: {len(emendas)}")
print(f"Emendas suspeitas: {len(suspeitas)}")
print(f"Não empenhadas: {len(nao_emp)}")