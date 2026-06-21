# Identificação do município
CODIGO_IBGE = "3515707"
NOME_MUNICIPIO = "Ferraz de Vasconcelos"
CNPJ_MUNICIPIO = "46523197000144"
UF = "SP"

# API SICONFI
BASE_URL = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"

# Anos que vamos coletar
ANOS = [2021, 2022, 2023, 2024]

# Tipos de relatório
RELATORIOS = {
    "RREO": "Relatório Resumido de Execução Orçamentária",
    "RGF":  "Relatório de Gestão Fiscal",
    "DCA":  "Declaração de Contas Anuais",
}