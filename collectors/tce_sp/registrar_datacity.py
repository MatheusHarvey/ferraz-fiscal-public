from pathlib import Path
from datetime import date

DOCS_DIR = Path("docs")

relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

adicao = """

### 9.4 DATACITY — Linha do tempo de contratos identificados

Com base nos dados do TCE-SP e do Portal da Transparência Municipal de 
Ferraz de Vasconcelos, foram identificados os seguintes contratos:

| Contrato | Ano | Objeto | Valor Contratado | Empenhos identificados | Total empenhado |
|---|---|---|---|---|---|
| 161/2016 | 2016 | Monitoramento de tráfego (radares) | não localizado | 1 (2020) | R$ 13.556,80 |
| 243/2020 | 2020 | Fornecimento e instalação de luminárias | R$ 1.964.132,00 | múltiplos | R$ 1.964.132,00 |
| 111/2021 | 2021 | Fornecimento e instalação de luminárias | R$ 1.479.545,04 | múltiplos | R$ 1.479.545,04 |
| 189/2021 | 2021 | Apoio técnico e manutenção de rede | R$ 1.164.000,00 | 4 | R$ 863.423,82 |
| 329/2022 | 2022 | Monitoramento e fiscalização viária | R$ 3.540.000,00 | 1 | R$ 2.360.000,00 |

**65 empenhos (R$ 43,6 milhões)** não puderam ser vinculados a um contrato 
específico nos registros disponíveis, incluindo todos os pagamentos de 2024 e 2025.

**Indícios identificados:**

1. **Contrato 161/2016 com vigência superior a 4 anos** — O 4º aditivo 
   aparece em 2020 e o 9º aditivo em 2022, indicando que um único contrato 
   de 2016 foi utilizado por pelo menos 6 anos, violando o limite de 5 anos 
   para contratos de serviços continuados (Lei 14.133/2021, Art. 106).

2. **Pagamentos sem referência contratual clara** — R$ 43,6 milhões em 
   65 empenhos entre 2020 e 2025 sem indicação do número do contrato nos 
   históricos de empenho.

3. **Crescimento de 140% em 2025** — Novo objeto contratual "Gerenciamento 
   e Implantação de Soluções Tecnológicas Integradas" com valores crescentes 
   sem licitação específica identificada.

4. **Termos de indenização recorrentes** — 3 ocorrências de "Termos de 
   Indenização" e "Termos de Ajuste de Contas" totalizando R$ 630.784,34, 
   indicando regularizações retroativas de pagamentos não previstos.

**Documentos obtidos via Portal da Transparência Municipal:**
- Contrato 329/2022 + 2º e 3º termos aditivos
- Contrato 189/2021 + termos aditivos
- Contratos 111/2021 e 243/2020

**Recomendação:** análise dos PDFs obtidos para verificar valores originais 
vs aditivos e solicitar via LAI os contratos anteriores a 2020.
"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    adicao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print(f"Relatório atualizado: {relatorio.name}")