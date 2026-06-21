import pandas as pd
from pathlib import Path
from loguru import logger

DESPESAS_DIR = Path("data/raw/tce_sp/conjunto-dados/despesas/despesas-csv")
PROCESSED_DIR = Path("data/processed/tce_sp")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

CODIGO_FERRAZ = "3515707"
CHUNKSIZE = 50000

COLUNAS_UTEIS = [
    "ano_exercicio",
    "ds_municipio",
    "ds_orgao",
    "mes_referencia",
    "mes_ref_extenso",
    "tp_despesa",
    "nr_empenho",
    "tp_identificador_despesa",
    "nr_identificador_despesa",
    "ds_despesa",
    "dt_emissao_despesa",
    "vl_despesa",
    "ds_funcao_governo",
    "ds_subfuncao_governo",
    "ds_modalidade_lic",
    "ds_elemento",
    "historico_despesa",
]

def processar_ano(ano: int) -> int:
    caminho = DESPESAS_DIR / f"despesas-{ano}.csv"
    if not caminho.exists():
        logger.warning(f"Arquivo não encontrado: {caminho.name}")
        return 0

    logger.info(f"Processando {caminho.name}...")
    total = 0
    frames = []

    for i, chunk in enumerate(pd.read_csv(
        caminho,
        sep=";",
        encoding="latin-1",
        dtype=str,
        chunksize=CHUNKSIZE,
        usecols=lambda c: c in COLUNAS_UTEIS + ["codigo_municipio_ibge"],
    )):
        ferraz = chunk[chunk["codigo_municipio_ibge"].astype(str).str.strip() == CODIGO_FERRAZ]
        if not ferraz.empty:
            frames.append(ferraz)
            total += len(ferraz)

        if i % 20 == 0:
            logger.info(f"  chunk {i} — {total} registros de Ferraz até agora")

    if frames:
        df = pd.concat(frames, ignore_index=True)
        saida = PROCESSED_DIR / f"despesas_tce_{ano}.csv"
        df.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
        logger.success(f"Salvo: {saida.name} — {len(df)} registros")
        return len(df)

    logger.warning(f"Nenhum registro de Ferraz encontrado em {ano}")
    return 0

def main():
    anos = [2020, 2021, 2022, 2023, 2024, 2025]
    total_geral = 0

    for ano in anos:
        total = processar_ano(ano)
        total_geral += total

    logger.success(f"Concluído! Total geral: {total_geral} registros")
    print(f"\nTotal de registros de Ferraz extraídos: {total_geral}")

if __name__ == "__main__":
    main()