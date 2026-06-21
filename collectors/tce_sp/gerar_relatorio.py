from pathlib import Path
from datetime import date
import pandas as pd

PROCESSED_DIR = Path("../../data/processed/tce_sp")
DOCS_DIR = Path("../../docs")

df = pd.read_csv(
    PROCESSED_DIR / "suspeitos_enriquecidos.csv",
    sep=";", encoding="utf-8-sig"
)

hoje = date.today().strftime("%d/%m/%Y")

linhas = []
linhas.append(f"# Relatório de Indícios de Irregularidade")
linhas.append(f"**Município:** Ferraz de Vasconcelos — SP")
linhas.append(f"**Período analisado:** 2022–2024")
linhas.append(f"**Data do relatório:** {hoje}")
linhas.append(f"**Fonte dos dados:** TCE-SP / Portal da Transparência Municipal")
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 1. Contexto")
linhas.append("")
linhas.append(
    "Este relatório foi gerado automaticamente pelo Ferraz Fiscal, "
    "ferramenta local de auditoria cívica das finanças públicas de Ferraz de Vasconcelos. "
    "Os dados foram obtidos do Portal da Transparência Municipal do TCE-SP e cruzados "
    "com informações da Receita Federal."
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
    "configurando possível fracionamento ilegal de despesa."
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 3. Achados")
linhas.append("")

# Total
total_valor = df["valor_total"].sum()
linhas.append(f"**Total de casos suspeitos:** {len(df)}")
linhas.append(f"**Valor total envolvido:** R$ {total_valor:,.2f}")
linhas.append("")

# Destaque crítico
linhas.append("### 3.1 Empresa inativa contratada — irregularidade grave")
linhas.append("")
linhas.append(
    "A empresa **E DE SOUZA LOPES** (CNPJ 42.041.320/0001-30), com situação "
    "cadastral **BAIXADA** na Receita Federal, recebeu **4 contratos** por dispensa "
    "de licitação em 2024, totalizando **R$ 102.149,49**. "
    "A contratação de empresa inativa é vedada pela legislação e configura "
    "irregularidade passível de responsabilização dos gestores envolvidos."
)
linhas.append("")

# Tabela de casos
linhas.append("### 3.2 Casos suspeitos de fracionamento")
linhas.append("")
linhas.append("| Empresa | CNPJ | Município | Situação | Ano | Contratos | Valor Total |")
linhas.append("|---|---|---|---|---|---|---|")

for _, row in df.iterrows():
    situacao = str(row.get("situacao_receita", "")).strip()
    municipio = str(row.get("municipio", "")).strip()
    uf = str(row.get("uf", "")).strip()
    local = f"{municipio}/{uf}" if municipio else "não consultado"
    alerta = " 🔴" if "BAIXADA" in situacao.upper() or "INAPTA" in situacao.upper() else ""
    linhas.append(
        f"| {row['nome_contrato']} "
        f"| {row['cnpj']} "
        f"| {local} "
        f"| {situacao}{alerta} "
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
    "1. **Verificar a legalidade dos contratos** com E DE SOUZA LOPES — "
    "empresa baixada não pode ser contratada pelo poder público."
)
linhas.append(
    "2. **Apurar possível fracionamento** nos contratos com BERTY CONSTRUÇÕES (7x), "
    "THREE F ENGENHARIA (5x) e W & MACEDO ELÉTRICA (4x) em 2024."
)
linhas.append(
    "3. **Solicitar via LAI** os processos administrativos referentes às dispensas "
    "identificadas para verificar a motivação de cada contratação."
)
linhas.append(
    "4. **Encaminhar ao TCE-SP** denúncia formal com os dados deste relatório "
    "em: https://www.tce.sp.gov.br/fale-conosco"
)
linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append("## 5. Pendências")
linhas.append("")
linhas.append(
    "Os seguintes CNPJs não puderam ser consultados automaticamente por limite "
    "de requisições nas APIs gratuitas. Recomenda-se consulta manual em "
    "https://servicos.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp:"
)
linhas.append("")

nao_encontrados = df[df["situacao_receita"] == "não encontrado"]
for _, row in nao_encontrados.iterrows():
    linhas.append(f"- **{row['nome_contrato']}** — CNPJ: {row['cnpj']}")

linhas.append("")
linhas.append("---")
linhas.append("")
linhas.append(
    "*Relatório gerado pelo Ferraz Fiscal — ferramenta de auditoria cívica. "
    "Os dados são públicos e obtidos de fontes oficiais. "
    "Este documento não substitui análise jurídica especializada.*"
)

# Salva
saida = DOCS_DIR / f"relatorio_irregularidades_{date.today().strftime('%Y%m%d')}.md"
saida.write_text("\n".join(linhas), encoding="utf-8")
print(f"Relatório gerado: {saida}")
print(f"Total de casos: {len(df)}")
print(f"Valor total envolvido: R$ {total_valor:,.2f}")