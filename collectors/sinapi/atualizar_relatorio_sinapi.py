from pathlib import Path
from datetime import date

DOCS_DIR = Path("docs")

relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

nova_secao = """
---

## 10. Análise de preços — SINAPI vs contratos CASAMAX

### 10.1 Referência de preços SINAPI para CBUQ — São Paulo

O SINAPI (Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil)
é o referencial oficial de preços utilizado pelo TCE-SP para auditar obras públicas.
Os preços abaixo foram extraídos dos relatórios mensais para São Paulo, sem desoneração:

| Período | CBUQ Faixa C CAP 30/45 | CBUQ Faixa C CAP 50/70 | CBUQ Binder |
|---|---|---|---|
| Jun/2022 | R$ 500,25/t | R$ 510,00/t | R$ 447,18/t |
| Dez/2022 | R$ 513,98/t | R$ 524,00/t | R$ 459,46/t |
| Jun/2023 | R$ 490,44/t | R$ 500,00/t | R$ 438,42/t |
| Dez/2023 | R$ 502,70/t | R$ 512,50/t | R$ 449,38/t |

### 10.2 Contratos CASAMAX — concreto usinado

A CASAMAX COMERCIAL E SERVIÇOS LTDA (CNPJ 08.183.516/0001-20) firmou
**8 contratos** de aquisição de concreto usinado entre 2022 e 2024,
totalizando **R$ 9.184.067,46**, classificados como "Outros materiais de consumo".

| Período | Valor contratado | Tonelagem estimada (SINAPI) |
|---|---|---|
| 1º sem/2022 | R$ 699.541,50 | ~1.398t |
| 2º sem/2022 | R$ 2.139.774,00 | ~4.163t |
| 2º sem/2022 | R$ 1.329.951,84 | ~2.588t |
| 2º sem/2022 | R$ 799.946,28 | ~1.556t |
| 2º sem/2022 | R$ 479.528,84 | ~933t |
| 1º sem/2023 | R$ 1.499.723,00 | ~3.058t |
| 2º sem/2023 | R$ 2.207.637,00 | ~4.501t |
| 2º sem/2023 | R$ 27.965,00 | ~56t |
| **Total** | **R$ 9.184.067,46** | **~18.253t estimadas** |

### 10.3 Limitações da análise e próximos passos

A comparação direta com o SINAPI não é possível sem as quantidades reais
em toneladas, pois os contratos registrados no TCE-SP não discriminam
quantidade — apenas o valor total. Além disso, contratos de pavimentação
frequentemente incluem transporte e aplicação além do material.

**Para uma análise conclusiva, é necessário solicitar via LAI:**
1. Notas fiscais detalhadas de cada contrato com quantidade em toneladas
2. Memória de cálculo dos contratos (planilha orçamentária)
3. Medições de serviços executados

Caso as notas fiscais indiquem preço por tonelada acima do SINAPI,
configura-se superfaturamento passível de responsabilização dos gestores.

### 10.4 Composições SINAPI para pavimentação completa

Para contratos que incluem material + aplicação, o referencial correto é:

| Serviço | Unidade | Custo SINAPI jun/2022 |
|---|---|---|
| Execução de pavimento com CBUQ — rolamento | m³ | R$ 1.427,93 |
| Execução de tapa-buraco com concreto asfáltico | m³ | R$ 1.711,57 |
| Usinagem de CBUQ CAP 50/70 — rolamento | t | R$ 517,41 |
| Usinagem de CBUQ CAP 50/70 — binder | t | R$ 479,49 |
| Fresagem de pavimento asfáltico (até 5cm) | m² | R$ 8,03 |

"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    nova_secao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print(f"Relatório atualizado: {relatorio.name}")