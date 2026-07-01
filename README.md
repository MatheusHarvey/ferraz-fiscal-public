# Ferraz Fiscal

Ferramenta de auditoria cívica independente das finanças públicas de **Ferraz de Vasconcelos — SP**.

## O que é isso?

Um cidadão comum se perguntou onde vai o imposto municipal. Baixou dados públicos, rodou scripts e encontrou indícios de irregularidades em contratos públicos de 2020 a 2026.

## Achados principais

| # | Achado | Valor | Gravidade |
|---|---|---|---|
| 1 | Classificação indevida — CBUQ como material de consumo | R\$ 24,8mi | 🔴 Crítico |
| 2 | DATACITY — aditivos sucessivos e pagamentos sem contrato | R\$ 46,9mi | 🔴 Alto |
| 3 | Fracionamento de despesa | R\$ 899k | 🟠 Médio |
| 4 | Locações com indícios de direcionamento | R\$ 2,7mi | 🟠 Médio |

Denúncia formal protocolada no **TCE-SP** em julho de 2026.

## Fontes de dados

Todos os dados são **públicos e verificáveis**:

- [TCE-SP / SAGRES](https://transparencia.tce.sp.gov.br)
- [SICONFI / STN](https://siconfi.tesouro.gov.br)
- [Portal da Transparência Federal](https://portaldatransparencia.gov.br)
- [Portal da Transparência Municipal de Ferraz](https://transparencia.ferrazdevasconcelos.sp.gov.br)
- [SINAPI / CEF](https://www.caixa.gov.br/site/paginas/downloads.aspx)
- [IBGE Cidades](https://cidades.ibge.gov.br)
- [DATASUS](https://datasus.saude.gov.br)

## Estrutura do projeto

\ferraz-fiscal/
├── collectors/          # Scripts de coleta e análise
│   ├── siconfi/         # Receitas e despesas orçamentárias
│   ├── tce_sp/          # Licitações, contratos e despesas
│   ├── portal_federal/  # Convênios e emendas federais
│   ├── transparencia_ferraz/ # Portal municipal
│   ├── sinapi/          # Preços de referência de obras
│   ├── ibge/            # Indicadores socioeconômicos
│   └── datasus/         # Indicadores de saúde
├── dashboard/           # Dashboard Streamlit interativo
│   └── app.py
├── data/processed/      # Dados processados prontos para análise
└── docs/                # Relatório e resumo executivo
\
## Como rodar

\\ash
# Clonar o repositório
git clone https://github.com/MatheusHarvey/ferraz-fiscal-public.git
cd ferraz-fiscal-public

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Rodar o dashboard
streamlit run dashboard/app.py
\
## Documentos

- [Relatório completo de indícios](docs/relatorio_irregularidades_20260620.md)
- [Resumo executivo](docs/resumo_executivo_tce_sp.md)

## Metodologia

Análise de dados públicos com processamento automatizado em Python.
Cruzamento de múltiplas fontes oficiais para identificação de padrões de irregularidade.

## Aviso legal

Este projeto é uma iniciativa cívica independente. Os dados são públicos e verificáveis.
Os achados constituem **indícios** de irregularidade — a apuração formal compete ao TCE-SP.

---

*Transparência pública é um direito de todo cidadão.*
