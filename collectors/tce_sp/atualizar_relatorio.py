from pathlib import Path
from datetime import date
import pandas as pd

PROCESSED_DIR = Path("../../data/processed/tce_sp")
DOCS_DIR = Path("../../docs")

# Carrega dados
frac = pd.read_csv(PROCESSED_DIR / "suspeitos_fracionamento.csv", sep=";", encoding="utf-8-sig")
cnpjs = pd.read_csv(
    PROCESSED_DIR / "cnpjs_enriquecidos.csv",
    sep=";",
    encoding="utf-8-sig",
    dtype=str,
    on_bad_lines="skip",
    engine="python",
)

# Mescla
df = frac.merge(cnpjs, left_on="CNPJ da empresa contratada", right_on="cnpj", how="left")

hoje = date.today().strftime("%d/%m/%Y")

linhas = []
linhas.append("# Relatório de Indícios de Irregularidade")
linhas.append(f"**Município:** Ferraz de Vasconcelos — SP")
linhas.append(f"**Período analisado:** 2022–2024")
linhas.append(f"**Data do relatório:** {hoje}")
linhas.append(f"**Fonte dos dados:** TCE-SP · Portal da Transparência Municipal · Receita Federal")
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 1. Contexto")
linhas.append("")
linhas.append(
    "Este relatório foi gerado pelo Ferraz Fiscal, ferramenta local de auditoria cívica "
    "das finanças públicas de Ferraz de Vasconcelos. Os dados foram obtidos do Portal da "
    "Transparência Municipal do TCE-SP, cruzados com informações da Receita Federal."
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 2. Metodologia")
linhas.append("")
linhas.append(
    "Foram analisados contratos firmados por dispensa de licitação entre 2022 e 2024. "
    "Identificaram-se fornecedores com múltiplos contratos no mesmo ano cujos valores somados "
    "ultrapassam o limite legal de R$ 50.000 (Lei 14.133/2021, Art. 75), "
    "configurando possível fracionamento ilegal de despesa. "
    "Os CNPJs identificados foram consultados na Receita Federal para verificação de "
    "situação cadastral, localização e compatibilidade de atividade."
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 3. Achados")
linhas.append("")
total_valor = frac["valor_total"].sum()
linhas.append(f"**Total de casos suspeitos de fracionamento:** {len(frac)}")
linhas.append(f"**Valor total envolvido:** R$ {total_valor:,.2f}")
linhas.append(f"**Concentração:** 9 dos 10 casos ocorreram em 2024")
linhas.append("")

# Achado 1 - Inapta
linhas.append("### 3.1 Empresa inapta contratada")
linhas.append("")
linhas.append(
    "A empresa **TEC CONST EMPREENDIMENTOS** (CNPJ 03.866.882/0001-60) consta como "
    "**INAPTA** na Receita Federal desde 12/05/2026. Os contratos foram firmados em 2022, "
    "anteriores à inaptidão formal. Recomenda-se verificar se já havia pendências fiscais "
    "no período da contratação, especialmente débitos com a Receita Federal ou FGTS, "
    "que poderiam impedir a habilitação em certames públicos."
)
linhas.append("")

# Achado 2 - Atividade incompatível
linhas.append("### 3.2 Empresas com atividade incompatível com o objeto contratado")
linhas.append("")
linhas.append("Duas empresas foram contratadas para obras de construção/engenharia, "
              "porém possuem CNAE principal incompatível com esse objeto:")
linhas.append("")
linhas.append("- **W & MACEDO ELÉTRICA LTDA** (CNPJ 29.179.763/0001-23) — "
              "CNAE: comércio varejista de material elétrico. "
              "Recebeu 4 contratos de obras de engenharia em 2024, totalizando R$ 83.807,77.")
linhas.append("- **CARLOS ALEXANDRO DE OLIVEIRA ARRUDA** (CNPJ 31.512.425/0001-03) — "
              "CNAE: atividades auxiliares de transportes terrestres. "
              "Recebeu 2 contratos de obras de construção em 2024, totalizando R$ 64.467,45. "
              "Registrada em São Paulo/SP.")
linhas.append("")

# Achado 3 - Empresa recém-criada
linhas.append("### 3.3 Empresa recém-criada contratada imediatamente")
linhas.append("")
linhas.append(
    "A empresa **JA RODRIGUES ARQUITETURA E ENGENHARIA LTDA** (CNPJ 55.871.049/0001-01) "
    "foi aberta em **10/07/2024** e já recebeu 2 contratos por dispensa no mesmo ano, "
    "totalizando R$ 69.940,89. Empresa registrada em Suzano/SP. "
    "A contratação imediata de empresa recém-constituída, sem histórico de execução, "
    "é indício de direcionamento de contrato."
)
linhas.append("")

# Achado 4 - Fracionamento
linhas.append("### 3.4 Casos suspeitos de fracionamento de despesa")
linhas.append("")
linhas.append(
    "Os seguintes fornecedores receberam múltiplos contratos por dispensa no mesmo ano, "
    "com valores individuais abaixo do limite legal mas soma superior a R$ 50.000, "
    "caracterizando possível fracionamento vedado pelo Art. 20 da Lei 14.133/2021:"
)
linhas.append("")
linhas.append("| Empresa | Município | Situação | Ano | Contratos | Valor Total |")
linhas.append("|---|---|---|---|---|---|")

for _, row in df.sort_values("valor_total", ascending=False).iterrows():
    municipio = str(row.get("municipio", "")).strip()
    uf = str(row.get("uf", "")).strip()
    local = f"{municipio}/{uf}" if municipio and municipio != "**" else "não consultado"
    situacao = str(row.get("situacao", "")).strip()
    linhas.append(
        f"| {row['Nome da empresa contratada']} "
        f"| {local} "
        f"| {situacao} "
        f"| {row['ano']} "
        f"| {int(row['qtd_contratos'])}x "
        f"| R$ {row['valor_total']:,.2f} |"
    )

linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 4. Recomendações")
linhas.append("")
linhas.append(
    "1. **Solicitar via LAI** os processos administrativos das dispensas identificadas "
    "para verificar motivação, documentação de habilitação e notas fiscais."
)
linhas.append(
    "2. **Verificar habilitação** de TEC CONST e W & MACEDO nos processos de 2022 e 2024 — "
    "especialmente certidões negativas de débito exigidas na contratação."
)
linhas.append(
    "3. **Investigar JA RODRIGUES** — empresa aberta e contratada no mesmo mês "
    "é indício forte de direcionamento."
)
linhas.append(
    "4. **Apurar fracionamento** em BERTY CONSTRUÇÕES (7 contratos, R$ 150k) "
    "e THREE F ENGENHARIA (5 contratos, R$ 93k) — casos mais expressivos."
)
linhas.append(
    "5. **Encaminhar ao TCE-SP** denúncia formal com os dados deste relatório: "
    "https://www.tce.sp.gov.br/fale-conosco"
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 5. Próximas investigações")
linhas.append("")
linhas.append("- 29 dispensas de **locação de imóveis** — análise em andamento")
linhas.append("- 549 dispensas de **medicamentos** — análise pendente")
linhas.append("- Monitoramento de **gastos com pessoal** (crescimento de 5pp em 2022–2023)")
linhas.append("- Monitoramento de **gastos com saúde** (flertando com o mínimo de 15%)")
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append(
    "*Relatório gerado pelo Ferraz Fiscal — ferramenta de auditoria cívica local. "
    "Dados públicos obtidos de fontes oficiais. "
    "Este documento não substitui análise jurídica especializada.*"
)

# Salva — substitui o anterior
saida = DOCS_DIR / f"relatorio_irregularidades_{date.today().strftime('%Y%m%d')}.md"
saida.write_text("\n".join(linhas), encoding="utf-8")
print(f"Relatório atualizado: {saida}")
print(f"Casos documentados: {len(df)}")
print(f"Valor total: R$ {total_valor:,.2f}")