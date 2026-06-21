import requests
import pandas as pd
from pathlib import Path
from loguru import logger
import time

PROCESSED_DIR = Path("../../data/processed/tce_sp")

def consultar_cnpj(cnpj: str) -> dict:
    """Consulta dados da empresa via CNPJ.ws."""
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    try:
        r = requests.get(
            f"https://publica.cnpj.ws/cnpj/{cnpj_limpo}",
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if r.status_code == 200:
            dados = r.json()
            # Adapta estrutura diferente do CNPJ.ws
            estabelecimento = dados.get("estabelecimento", {})
            return {
                "situacao": estabelecimento.get("situacao_cadastral", ""),
                "nome": dados.get("razao_social", ""),
                "municipio": estabelecimento.get("cidade", {}).get("nome", "") if estabelecimento.get("cidade") else "",
                "uf": estabelecimento.get("estado", {}).get("sigla", "") if estabelecimento.get("estado") else "",
                "abertura": estabelecimento.get("data_inicio_atividade", ""),
                "tipo": dados.get("natureza_juridica", {}).get("descricao", "") if dados.get("natureza_juridica") else "",
                "porte": dados.get("porte", {}).get("descricao", "") if dados.get("porte") else "",
                "atividade_principal": [{"text": dados.get("cnae_fiscal_descricao", "")}],
            }
        else:
            logger.warning(f"CNPJ {cnpj}: status {r.status_code}")
            return {}
    except Exception as e:
        logger.error(f"CNPJ {cnpj}: {e}")
        return {}

def main():
    df = pd.read_csv(
        PROCESSED_DIR / "suspeitos_fracionamento.csv",
        sep=";", encoding="utf-8-sig"
    )

    resultados = []

    for _, row in df.iterrows():
        cnpj = str(row["CNPJ da empresa contratada"]).strip()
        nome = str(row["Nome da empresa contratada"]).strip()
        logger.info(f"Consultando: {nome} — {cnpj}")

        dados = consultar_cnpj(cnpj)

        resultados.append({
            "nome_contrato":    nome,
            "cnpj":             cnpj,
            "ano":              row["ano"],
            "qtd_contratos":    row["qtd_contratos"],
            "valor_total":      row["valor_total"],
            "situacao_receita": dados.get("situacao", "não encontrado"),
            "razao_social":     dados.get("nome", ""),
            "municipio":        dados.get("municipio", ""),
            "uf":               dados.get("uf", ""),
            "abertura":         dados.get("abertura", ""),
            "tipo":             dados.get("tipo", ""),
            "porte":            dados.get("porte", ""),
            "atividade":        dados.get("atividade_principal", [{}])[0].get("text", "") if dados.get("atividade_principal") else "",
        })

        time.sleep(1.5)  # respeita o rate limit da API

    df_result = pd.DataFrame(resultados)

    print("\n" + "=" * 80)
    print("EMPRESAS SUSPEITAS DE FRACIONAMENTO — DADOS DA RECEITA FEDERAL")
    print("=" * 80)

    for _, row in df_result.iterrows():
        distancia = "⚠ FORA DA REGIÃO" if row["uf"] not in ["SP", ""] and row["municipio"] != "FERRAZ DE VASCONCELOS" else ""
        inativa = "🔴 INATIVA" if "INAPTA" in str(row["situacao_receita"]).upper() or "BAIXADA" in str(row["situacao_receita"]).upper() else ""

        print(f"\nEmpresa:   {row['nome_contrato']}")
        print(f"CNPJ:      {row['cnpj']}")
        print(f"Situação:  {row['situacao_receita']} {inativa}")
        print(f"Município: {row['municipio']} — {row['uf']} {distancia}")
        print(f"Abertura:  {row['abertura']} | Porte: {row['porte']}")
        print(f"Atividade: {row['atividade']}")
        print(f"Ano:       {row['ano']} | Contratos: {int(row['qtd_contratos'])}x | Total: R$ {row['valor_total']:,.2f}")
        print("-" * 80)

    saida = PROCESSED_DIR / "suspeitos_enriquecidos.csv"
    df_result.to_csv(saida, index=False, encoding="utf-8-sig", sep=";")
    logger.success(f"Salvo em: {saida}")

if __name__ == "__main__":
    main()