from pathlib import Path
from datetime import date, datetime
import pandas as pd

PROCESSED_DIR = Path("../../data/processed/tce_sp")
DOCS_DIR = Path("../../docs")

# Carrega dados
frac = pd.read_csv(PROCESSED_DIR / "suspeitos_fracionamento.csv", sep=";", encoding="utf-8-sig")
cnpjs = pd.read_csv(PROCESSED_DIR / "cnpjs_enriquecidos.csv", sep=";", encoding="utf-8-sig", dtype=str, on_bad_lines="skip", engine="python")
loc = pd.read_csv(PROCESSED_DIR / "locacoes_imoveis.csv", sep=";", encoding="utf-8-sig", dtype=str)

# Converte valor locações
loc["Valor total do contrato"] = pd.to_numeric(
    loc["Valor total do contrato"].str.replace(",", "."), errors="coerce"
)

# Calcula custo mensal
def calcular_meses(inicio, fim):
    try:
        d1 = datetime.strptime(str(inicio).strip(), "%d/%m/%Y")
        d2 = datetime.strptime(str(fim).strip(), "%d/%m/%Y")
        meses = (d2.year - d1.year) * 12 + (d2.month - d1.month)
        return max(meses, 1)
    except:
        return None

loc["meses_vigencia"] = loc.apply(
    lambda r: calcular_meses(
        r["Vigência do contrato - Data início"],
        r["Vigência do contrato - Data Término"]
    ), axis=1
)

loc["custo_mensal"] = loc.apply(
    lambda r: r["Valor total do contrato"] / r["meses_vigencia"]
    if r["meses_vigencia"] else None, axis=1
)

df = frac.merge(cnpjs, left_on="CNPJ da empresa contratada", right_on="cnpj", how="left")

hoje = date.today().strftime("%d/%m/%Y")
total_frac = frac["valor_total"].sum()
total_loc = loc["Valor total do contrato"].sum()
total_geral = total_frac + total_loc

linhas = []
linhas.append("# Relatório de Indícios de Irregularidade")
linhas.append(f"**Município:** Ferraz de Vasconcelos — SP")
linhas.append(f"**Período analisado:** 2021–2024")
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
    "Transparência Municipal do TCE-SP e cruzados com informações da Receita Federal."
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 2. Metodologia")
linhas.append("")
linhas.append(
    "Foram analisados contratos firmados por dispensa de licitação entre 2021 e 2024. "
    "Identificaram-se dois grupos de irregularidades: (1) fornecedores com múltiplos contratos "
    "no mesmo ano cujos valores somados ultrapassam o limite legal de R$ 50.000, configurando "
    "possível fracionamento ilegal; (2) locações de imóveis por dispensa com indícios de "
    "direcionamento a pessoas com vínculos familiares."
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 3. Visão Geral dos Achados")
linhas.append("")
linhas.append(f"| Categoria | Contratos | Valor Total |")
linhas.append(f"|---|---|---|")
linhas.append(f"| Suspeitos de fracionamento | {len(frac)} casos | R$ {total_frac:,.2f} |")
linhas.append(f"| Locações de imóveis suspeitas | {len(loc)} contratos | R$ {total_loc:,.2f} |")
linhas.append(f"| **Total geral** | | **R$ {total_geral:,.2f}** |")
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 4. Fracionamento de Despesa")
linhas.append("")
linhas.append(
    "Os seguintes fornecedores receberam múltiplos contratos por dispensa no mesmo ano, "
    "com valores individuais abaixo do limite legal mas soma superior a R$ 50.000, "
    "caracterizando possível fracionamento vedado pelo Art. 20 da Lei 14.133/2021:"
)
linhas.append("")
linhas.append(f"**Total envolvido: R$ {total_frac:,.2f} | 10 casos | concentrados em 2024**")
linhas.append("")

linhas.append("### 4.1 Empresas com atividade incompatível")
linhas.append("")
linhas.append(
    "- **W & MACEDO ELÉTRICA LTDA** (CNPJ 29.179.763/0001-23) — CNAE: comércio varejista "
    "de material elétrico. Contratada para obras de engenharia. "
    "4 contratos em 2024 — R$ 83.807,77."
)
linhas.append(
    "- **CARLOS ALEXANDRO DE OLIVEIRA ARRUDA** (CNPJ 31.512.425/0001-03) — CNAE: transportes "
    "terrestres. Contratado para obras de construção. Registrado em São Paulo/SP. "
    "2 contratos em 2024 — R$ 64.467,45."
)
linhas.append("")
linhas.append("### 4.2 Empresa recém-criada contratada imediatamente")
linhas.append("")
linhas.append(
    "**JA RODRIGUES ARQUITETURA E ENGENHARIA LTDA** (CNPJ 55.871.049/0001-01) — "
    "aberta em 10/07/2024 e já contratada no mesmo ano. "
    "2 contratos — R$ 69.940,89. Registrada em Suzano/SP."
)
linhas.append("")
linhas.append("### 4.3 Empresa inapta")
linhas.append("")
linhas.append(
    "**TEC CONST EMPREENDIMENTOS** (CNPJ 03.866.882/0001-60) — inapta desde 12/05/2026. "
    "Contratos firmados em 2022. Recomenda-se verificar situação fiscal à época da contratação."
)
linhas.append("")
linhas.append("### 4.4 Tabela completa de casos suspeitos")
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
linhas.append("## 5. Locações de Imóveis por Dispensa")
linhas.append("")
linhas.append(
    f"Foram identificadas **{len(loc)} locações de imóveis** por dispensa de licitação "
    f"totalizando **R$ {total_loc:,.2f}**. "
    f"Do total, 87% dos contratos (R$ {loc[loc['CNPJ da empresa contratada'].isna()]['Valor total do contrato'].sum():,.2f}) "
    f"foram firmados com **pessoas físicas**, sem processo licitatório formal."
)
linhas.append("")
linhas.append("### 5.1 Possíveis vínculos familiares")
linhas.append("")
linhas.append(
    "Os seguintes pares de contratados compartilham sobrenome e tiveram contratos "
    "firmados na mesma data com valores idênticos ou próximos, sugerindo possível "
    "direcionamento a pessoas com vínculos familiares:"
)
linhas.append("")
linhas.append("| Contratados | Sobrenome | Data | Valor Total |")
linhas.append("|---|---|---|---|")
linhas.append("| BRAULIO BUENO DE ALMEIDA + SILVANA VALIERIS BUENO DE ALMEIDA | ALMEIDA | 19/04/2021 | R$ 450.000,00 |")
linhas.append("| SILVIO FRANCISCO CHAGAS + REGINA CLAUDINA DA CUNHA CHAGAS | CHAGAS | 20/05/2022 | R$ 222.015,90 |")
linhas.append("")
linhas.append("### 5.2 Maiores contratos de locação com custo mensal")
linhas.append("")
linhas.append("| Contratado | Valor Total | Vigência | Custo Mensal |")
linhas.append("|---|---|---|---|")
top5 = loc.nlargest(5, "Valor total do contrato")
for _, r in top5.iterrows():
    inicio = str(r.get("Vigência do contrato - Data início", "s/d")).strip()
    fim = str(r.get("Vigência do contrato - Data Término", "s/d")).strip()
    custo = f"R$ {r['custo_mensal']:,.2f}/mês" if pd.notna(r["custo_mensal"]) else "s/d"
    linhas.append(
        f"| {r['Nome da empresa contratada']} "
        f"| R$ {r['Valor total do contrato']:,.2f} "
        f"| {inicio} a {fim} "
        f"| {custo} |"
    )
linhas.append("")
linhas.append(
    "> **Nota:** A INDÚSTRIA E COMÉRCIO DE ALUMÍNIO ABC LTDA recebeu o maior contrato "
    "de locação (R$ 464.583,00) sem datas de vigência registradas, o que dificulta "
    "a verificação da regularidade do contrato."
)
linhas.append("")
linhas.append("### 5.3 Todos os contratos de locação")
linhas.append("")
linhas.append("| Contratado | Valor Total | Meses | Custo Mensal |")
linhas.append("|---|---|---|---|")
for _, r in loc.sort_values("Valor total do contrato", ascending=False).iterrows():
    meses = str(int(r["meses_vigencia"])) if pd.notna(r["meses_vigencia"]) else "s/d"
    custo = f"R$ {r['custo_mensal']:,.2f}/mês" if pd.notna(r["custo_mensal"]) else "s/d"
    linhas.append(
        f"| {r['Nome da empresa contratada']} "
        f"| R$ {r['Valor total do contrato']:,.2f} "
        f"| {meses} "
        f"| {custo} |"
    )
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 6. Recomendações")
linhas.append("")
linhas.append(
    "1. **Solicitar via LAI** os processos administrativos de todas as dispensas identificadas, "
    "especialmente as locações, verificando avaliações de valor de mercado e justificativas formais."
)
linhas.append(
    "2. **Investigar vínculos** entre os pares ALMEIDA e CHAGAS e agentes públicos "
    "da administração municipal no período das contratações."
)
linhas.append(
    "3. **Verificar habilitação** de W & MACEDO e CARLOS ALEXANDRO nos processos "
    "de 2024 — atividade declarada é incompatível com obras de engenharia."
)
linhas.append(
    "4. **Apurar fracionamento** em BERTY CONSTRUÇÕES (7 contratos, R$ 150k) "
    "e THREE F ENGENHARIA (5 contratos, R$ 93k)."
)
linhas.append(
    "5. **Encaminhar ao TCE-SP** denúncia formal: https://www.tce.sp.gov.br/fale-conosco"
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 7. Achados sem irregularidade")
linhas.append("")
linhas.append("### 7.1 Dispensas de medicamentos — gestão adequada")
linhas.append("")
linhas.append(
    "A análise das 607 dispensas de medicamentos identificadas entre 2020 e 2024 não revelou "
    "indícios de irregularidade. O volume elevado em 2024 (+972% em relação à média histórica) "
    "decorreu da consolidação de compras em poucos processos: 208 itens em 2 processos em março "
    "e 206 itens em 1 processo em dezembro. Padrão compatível com reposição semestral de estoque "
    "da farmácia municipal. **Avaliação: ponto positivo da gestão atual.**"
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 8. Próximas investigações")
linhas.append("")
linhas.append("- Monitoramento de **gastos com pessoal** (crescimento de 5pp em 2022–2023)")
linhas.append("- Monitoramento de **gastos com saúde** (próximo do mínimo de 15%)")
linhas.append("- Integração dos dados de **convênios federais** ao relatório")
linhas.append("- Incorporação dos achados ao **dashboard Streamlit**")
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append(
    "*Relatório gerado pelo Ferraz Fiscal — ferramenta de auditoria cívica local. "
    "Dados públicos obtidos de fontes oficiais. "
    "Este documento não substitui análise jurídica especializada.*"
)

# Remove relatório anterior e salva novo
for f in DOCS_DIR.glob("relatorio_irregularidades_*.md"):
    f.unlink()

saida = DOCS_DIR / f"relatorio_irregularidades_{date.today().strftime('%Y%m%d')}.md"
saida.write_text("\n".join(linhas), encoding="utf-8")
print(f"Relatório atualizado: {saida}")
print(f"Total geral documentado: R$ {total_geral:,.2f}")