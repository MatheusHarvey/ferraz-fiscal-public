from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed/portal_federal")
DOCS_DIR = Path("docs")

df = pd.read_csv(
    PROCESSED_DIR / "emendas_federais_ferraz.csv",
    sep=";", encoding="utf-8-sig"
)

for col in ["Valor Empenhado", "Valor Pago"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

emp = df[df["Fase da despesa"] == "Empenho"]

top_autores = emp.groupby("Nome do Autor da Emenda")["Valor Empenhado"].sum().sort_values(ascending=False).head(10)
top_fav = emp.groupby("Favorecido")["Valor Empenhado"].sum().sort_values(ascending=False).head(5)
por_ano = emp.groupby("Ano da Emenda")["Valor Empenhado"].sum()
por_tipo = emp.groupby("Tipo de Emenda")["Valor Empenhado"].sum().sort_values(ascending=False)

relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

adicao = f"""

---

## 12. Emendas Parlamentares Federais — 2020–2024

Fonte: Portal da Transparência Federal · Dados filtrados pelo código IBGE 3515707

### 12.1 Visão geral

| Indicador | Valor |
|---|---|
| Total de registros | 211 |
| Valor total empenhado | R$ 58.605.854,88 |
| Valor total pago | R$ 46.584.417,64 |

### 12.2 Evolução anual

| Ano | Valor Empenhado |
|---|---|
{"".join(f"| {ano} | R$ {valor:,.2f} |{chr(10)}" for ano, valor in por_ano.items() if valor > 0)}

**Crescimento expressivo em 2023–2024:** R$ 48 milhões em dois anos,
contra R$ 10,5 milhões nos três anos anteriores combinados.

### 12.3 Por tipo de emenda

| Tipo | Valor Empenhado |
|---|---|
{"".join(f"| {tipo} | R$ {valor:,.2f} |{chr(10)}" for tipo, valor in por_tipo.items())}

### 12.4 Top 10 autores de emendas

| Parlamentar | Valor Empenhado |
|---|---|
{"".join(f"| {autor} | R$ {valor:,.2f} |{chr(10)}" for autor, valor in top_autores.items())}

**Observação:** RODRIGO GAMBALE é o maior destinador individual de emendas
federais (R$ 12,0 milhões) e também aparece como vereador nas emendas
municipais — indicando atuação em dois níveis de governo.

### 12.5 Favorecidos

| Favorecido | Valor Empenhado |
|---|---|
{"".join(f"| {fav} | R$ {valor:,.2f} |{chr(10)}" for fav, valor in top_fav.items())}

### 12.6 Pontos de atenção

1. **Crescimento de 586% em 2023** — de R$ 2,9mi para R$ 20,1mi em um ano.
   Coincide com o pico de gastos da CASAMAX (R$ 32mi em 2023).

2. **R$ 27,9mi em Transferências Especiais** direto ao município — sem
   vinculação de finalidade, a prefeitura pode usar livremente.

3. **Emendas de Comissão de Saúde: R$ 10,3mi** — compatível com o aumento
   nos gastos de saúde identificados no AUDESP.

"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    adicao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print("Relatório atualizado com emendas federais!")
print(f"Total empenhado: R$ {df['Valor Empenhado'].sum():,.2f}")