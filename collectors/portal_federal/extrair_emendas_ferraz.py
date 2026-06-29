import pandas as pd
from pathlib import Path
from loguru import logger

RAW_DIR = Path("data/raw/portal_federal/emendas-parlamentares")
PROCESSED_DIR = Path("data/processed/portal_federal")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

CODIGO_FERRAZ = "3515707"
CHUNKSIZE = 50000

COLUNAS_UTEIS = [
    "Código da Emenda", "Ano da Emenda", "Nome do Autor da Emenda",
    "Número da emenda", "Tipo de Emenda", "Valor Empenhado", "Valor Pago",
    "Data Documento", "Município de aplicação do recurso",
    "Código IBGE do município de aplicação do recurso",
    "Fase da despesa", "Favorecido", "Órgão Superior",
    "Grupo Despesa", "Elemento Despesa", "Função", "SubFunção",
    "Ação", "Possui convênio?"
]

arquivos = sorted(RAW_DIR.glob("*.csv"))
todos = []

for arquivo in arquivos:
    ano = arquivo.name[:4]
    logger.info(f"Processando {arquivo.name}...")
    total = 0

    for i, chunk in enumerate(pd.read_csv(
        arquivo, sep=";", encoding="latin-1",
        dtype=str, chunksize=CHUNKSIZE,
        usecols=lambda c: c in COLUNAS_UTEIS + ["Código IBGE do município de aplicação do recurso"]
    )):
        ferraz = chunk[
            chunk["Código IBGE do município de aplicação do recurso"]
            .astype(str).str.strip() == CODIGO_FERRAZ
        ]
        if not ferraz.empty:
            todos.append(ferraz)
            total += len(ferraz)

        if i % 20 == 0 and i > 0:
            logger.info(f"  chunk {i} — {total} registros de Ferraz")

    logger.success(f"  {ano}: {total} registros")

if todos:
    df = pd.concat(todos, ignore_index=True)

    # Converte valores
    for col in ["Valor Empenhado", "Valor Pago"]:
        df[col] = pd.to_numeric(
            df[col].str.replace(".", "").str.replace(",", "."),
            errors="coerce"
        )

    saida = PROCESSED_DIR / "emendas_federais_ferraz.csv"
    df.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")

    print(f"\n{'='*60}")
    print(f"EMENDAS FEDERAIS — FERRAZ DE VASCONCELOS")
    print(f"{'='*60}")
    print(f"Total de registros: {len(df)}")
    print(f"Valor total empenhado: R$ {df['Valor Empenhado'].sum():,.2f}")
    print(f"Valor total pago: R$ {df['Valor Pago'].sum():,.2f}")

    print(f"\nPor fase de despesa:")
    print(df["Fase da despesa"].value_counts().to_string())

    print(f"\nPor tipo de emenda:")
    print(df["Tipo de Emenda"].value_counts().to_string())

    print(f"\nPor ano:")
    print(df.groupby("Ano da Emenda")["Valor Empenhado"].sum()
          .apply(lambda x: f"R$ {x:,.2f}").to_string())

    print(f"\nTop 10 autores por valor empenhado:")
    top = df[df["Fase da despesa"] == "Empenho"].groupby(
        "Nome do Autor da Emenda")["Valor Empenhado"].sum().sort_values(
        ascending=False).head(10)
    for autor, valor in top.items():
        print(f"  R$ {valor:>14,.2f}  {autor}")

    print(f"\nTop 10 favorecidos:")
    top_fav = df[df["Fase da despesa"] == "Empenho"].groupby(
        "Favorecido")["Valor Empenhado"].sum().sort_values(
        ascending=False).head(10)
    for fav, valor in top_fav.items():
        print(f"  R$ {valor:>14,.2f}  {fav}")

    print(f"\nSalvo em: {saida}")
else:
    print("Nenhum registro encontrado para Ferraz!")