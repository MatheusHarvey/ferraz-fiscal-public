from pathlib import Path
from datetime import date

DOCS_DIR = Path("docs")

# Localiza o relatório atual
relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

nova_secao = """
---

## 9. Fornecedores estratégicos — análise de despesas TCE-SP 2020–2025

### 9.1 DATACITY SERVIÇOS LTDA — R$ 46,9 milhões

**CNPJ:** 02.679.522/0001-97
**Serviços:** monitoramento de tráfego (radares), iluminação pública, soluções tecnológicas

| Ano | Valor Empenhado |
|---|---|
| 2020 | R$ 4.729.113,05 |
| 2021 | R$ 5.922.737,31 |
| 2022 | R$ 5.658.110,87 |
| 2023 | R$ 5.883.171,07 |
| 2024 | R$ 11.534.578,06 |
| 2025 | R$ 13.202.738,71 |

**Indícios identificados:**

- **Contrato 161/16 — ativo por pelo menos 4 anos com múltiplos aditivos.** O Contrato 161/2016 aparece com 4º aditivo em 2020 e 9º aditivo em 2022, indicando uso de um único contrato por quase uma década — prática vedada pela legislação vigente, que limita contratos de serviços continuados a 5 anos (Lei 14.133/2021, Art. 106).

- **Crescimento de 109% em 2024 e 140% em 2025** em relação à média histórica de R$ 5,5mi/ano. O novo objeto "Gerenciamento e Implantação de Soluções Tecnológicas Integradas" sugere expansão do escopo sem novo processo licitatório adequado.

- **R$ 1.610.915,87 em indenizações e termos de ajuste** — 10 ocorrências de pagamentos fora do contrato original, incluindo "Termos de Ajuste de Contas" e "Reempenhos", indicando regularizações retroativas de pagamentos.

**Recomendações:**
1. Solicitar via LAI os contratos 161/2016, 189/2021 e 329/2022 com todos os termos aditivos
2. Verificar se os aditivos respeitaram o limite de 25% do valor original (Lei 8.666/93)
3. Investigar a natureza dos termos de indenização e ajuste de contas

### 9.2 CASAMAX COMERCIAL E SERVIÇOS LTDA — R$ 87,5 milhões

**CNPJ:** 08.183.516/0001-20
**Serviços:** pavimentação asfáltica, fornecimento de CBUQ, tapa-buracos, obras em andamento

| Ano | Valor Empenhado |
|---|---|
| 2020 | R$ 4.452.672,40 |
| 2021 | R$ 4.766.256,06 |
| 2022 | R$ 34.520.040,70 |
| 2023 | R$ 32.049.640,77 |
| 2024 | R$ 7.610.331,31 |
| 2025 | R$ 4.101.555,93 |

**Observações:**

- Licitações regulares identificadas (concorrência, pregão eletrônico e presencial)
- Pico de R$ 66,5 milhões em 2022-2023 — compatível com obras de pavimentação de maior porte
- Sem dispensas expressivas identificadas
- **Monitoramento recomendado:** verificar se houve aditivos contratuais excessivos nas obras de 2022-2023 e se as medições de serviços executados foram auditadas pelo TCE-SP

"""

# Insere antes do rodapé
conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    nova_secao + "\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print(f"Relatório atualizado: {relatorio.name}")