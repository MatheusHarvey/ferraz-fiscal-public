import zipfile
from pathlib import Path
from loguru import logger

RAW_DIR = Path("../../data/raw/siconfi")

# Mapeamento: parte do nome do zip -> nome final do CSV
MAPEAMENTO = {
    "AnexoI-D": "despesas.csv",
    "AnexoI-E": "despesas_funcao.csv",
    "AnexoI-C": "receitas.csv",
}

def extrair_e_renomear(zip_path: Path):
    """Extrai um zip e renomeia o CSV interno para um nome descritivo."""
    nome_zip = zip_path.name
    pasta_destino = zip_path.parent

    # Descobre qual tipo de arquivo é pelo nome do zip
    nome_final = None
    for chave, nome in MAPEAMENTO.items():
        if chave in nome_zip:
            nome_final = nome
            break

    if not nome_final:
        logger.warning(f"Não reconhecido: {nome_zip}")
        return

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            # Pega o primeiro CSV dentro do zip
            csvs = [f for f in z.namelist() if f.endswith(".csv")]
            if not csvs:
                logger.warning(f"Nenhum CSV dentro de {nome_zip}")
                return

            # Extrai para pasta temporária e renomeia
            z.extract(csvs[0], pasta_destino)
            origem = pasta_destino / csvs[0]
            destino = pasta_destino / nome_final

            # Remove destino se já existir
            if destino.exists():
                destino.unlink()

            origem.rename(destino)
            logger.success(f"{nome_zip} → {nome_final}")

    except Exception as e:
        logger.error(f"Erro ao extrair {nome_zip}: {e}")

def main():
    zips = sorted(RAW_DIR.rglob("*.zip"))

    if not zips:
        logger.error("Nenhum arquivo ZIP encontrado em data/raw/siconfi/")
        return

    logger.info(f"Encontrados {len(zips)} arquivos ZIP")

    for zip_path in zips:
        extrair_e_renomear(zip_path)

    logger.success("Extração concluída!")

if __name__ == "__main__":
    main()