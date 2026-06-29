import pandas as pd
from pathlib import Path
from datetime import datetime

PROCESSED_DIR = Path("data/processed/transparencia_ferraz")
DOCS_DIR = Path("docs")

# Carrega o template preenchido
df = pd.read_excel(
    Path("data/processed/transparencia_ferraz/datacity_contratos_template.xlsx")
)

# Vamos usar os dados diretamente
contratos = {
    "329/2022": {
        "objeto": "Monitoramento e fiscalização de tráfego de veículos (radares)",
        "original": 3540000.00,
        "aditivos": [
            ("1º", 3845873.21, "30/08/2023", "30/08/2024"),
            ("2º", 4008420.38, "31/08/2024", "30/08/2025"),
            ("3º", 4230075.24, "31/08/2025", "30/08/2026"),
        ],
        "inicio": "31/08/2022",
        "fim_original": "31/08/2023",
    },
    "189/2021": {
        "objeto": "Apoio técnico tecnológico — manutenção preventiva e corretiva de rede",
        "original": 1164000.00,
        "aditivos": [
            ("1º", None, "25/08/2022", "24/08/2023"),
            ("3º", 1503224.73, "25/08/2023", "24/08/2024"),
            ("4º", 1570843.44, "25/08/2024", "24/08/2025"),
            ("5º", 1654407.60, "25/08/2025", "24/08/2026"),
        ],
        "inicio": "25/08/2021",
        "fim_original": "25/08/2022",
    },
    "243/2020": {
        "objeto": "Fornecimento e instalação de luminárias públicas LED",
        "original": 1964132.00,
        "aditivos": [
            ("1º", None, "04/02/2021", "03/08/2021"),
        ],
        "inicio": "04/11/2020",
        "fim_original": "04/02/2021",
    },
    "111/2021": {
        "objeto": "Fornecimento e instalação de luminárias de LED",
        "original": 1479545.04,
        "aditivos": [],
        "inicio": "23/06/2021",
        "fim_original": "23/06/2022",
    },
}

# Calcula totais e vigências
total_329 = 3540000 + 3845873.21 + 4008420.38 + 4230075.24
total_189 = 1164000 + 1503224.73 + 1570843.44 + 1654407.60
anos_329 = 4  # ago/2022 a ago/2026
anos_189 = 5  # ago/2021 a ago/2026

relatorio = sorted(DOCS_DIR.glob("relatorio_irregularidades_*.md"))[-1]
conteudo = relatorio.read_text(encoding="utf-8")

adicao = f"""

### 9.10 DATACITY — Análise dos contratos via PDFs (P012)

Análise dos documentos contratuais obtidos via Portal da Transparência
Municipal de Ferraz de Vasconcelos.

#### Contrato 329/2022 — Monitoramento de tráfego (radares)

**Objeto:** Contratação de empresa especializada para prestação de serviços
de monitoramento e fiscalização do tráfego de veículos nas vias do município,
compreendendo a disponibilização de infraestrutura, equipamentos, softwares,
materiais e mão de obra. Pregão Presencial nº 038/2021.

| Instrumento | Vigência | Valor |
|---|---|---|
| Contrato original | 31/08/2022 a 31/08/2023 | R$ 3.540.000,00 |
| 1º Aditivo | 30/08/2023 a 30/08/2024 | R$ 3.845.873,21 |
| 2º Aditivo | 31/08/2024 a 30/08/2025 | R$ 4.008.420,38 |
| 3º Aditivo | 31/08/2025 a 30/08/2026 | R$ 4.230.075,24 |
| **Total acumulado** | **4 anos** | **R$ {total_329:,.2f}** |

**🔴 Indício:** contrato com vigência de 12 meses prorrogado por mais 36 meses
via 3 aditivos sucessivos, totalizando **4 anos de vigência** (ago/2022 a ago/2026).
A Lei 14.133/2021 (Art. 106) limita contratos de serviços continuados a 5 anos.
Embora dentro do limite legal, cada aditivo representa reajuste de 4 a 9%,
acumulando **+19,5%** sobre o valor original em 3 anos.

#### Contrato 189/2021 — Apoio técnico e manutenção de rede

**Objeto:** Serviço de apoio técnico tecnológico — manutenção preventiva
e corretiva de rede.

| Instrumento | Vigência | Valor |
|---|---|---|
| Contrato original | 25/08/2021 a 25/08/2022 | R$ 1.164.000,00 |
| 1º Aditivo | 25/08/2022 a 24/08/2023 | não localizado |
| 3º Aditivo | 25/08/2023 a 24/08/2024 | R$ 1.503.224,73 |
| 4º Aditivo | 25/08/2024 a 24/08/2025 | R$ 1.570.843,44 |
| 5º Aditivo | 25/08/2025 a 24/08/2026 | R$ 1.654.407,60 |
| **Total parcial** | **5 anos** | **R$ {total_189:,.2f}** |

**🔴 Indício:** contrato de 2021 prorrogado via 5 aditivos até agosto de 2026,
totalizando **5 anos de vigência** — no limite máximo permitido pela Lei 14.133/2021.
O 2º aditivo não foi localizado nos documentos disponíveis, o que impede
a análise completa da evolução de valores.

#### Contratos de luminárias

| Contrato | Objeto | Valor Original | Vigência |
|---|---|---|---|
| 243/2020 | Luminárias públicas LED | R$ 1.964.132,00 | Nov/2020 a Ago/2021 |
| 111/2021 | Luminárias de LED | R$ 1.479.545,04 | Jun/2021 a Jun/2022 |

Dois contratos de luminárias em anos consecutivos para o mesmo fornecedor
e objeto similar — possível fracionamento ou substituição de contrato
sem novo processo licitatório.

#### Resumo dos achados P012

1. **Contrato 329/2022** — 4 anos via aditivos, acúmulo de R$ {total_329:,.2f}
2. **Contrato 189/2021** — 5 anos via aditivos, acúmulo de R$ {total_189:,.2f}
3. **2º aditivo do contrato 189/2021** — não localizado nos documentos públicos
4. **Contratos de luminárias duplicados** — objeto similar em anos consecutivos
5. **Reajustes acumulados** — 329/2022: +19,5% em 3 anos; 189/2021: +42% em 4 anos

**Recomendação:** incluir na denúncia ao TCE-SP a análise dos aditivos
e solicitar via LAI o 2º aditivo do contrato 189/2021 não localizado.
"""

conteudo = conteudo.replace(
    "*Relatório gerado pelo Ferraz Fiscal",
    adicao + "\n---\n\n*Relatório gerado pelo Ferraz Fiscal"
)

relatorio.write_text(conteudo, encoding="utf-8")
print("Relatório atualizado com análise dos contratos DATACITY!")
print(f"Contrato 329/2022 total: R$ {total_329:,.2f}")
print(f"Contrato 189/2021 total: R$ {total_189:,.2f}")