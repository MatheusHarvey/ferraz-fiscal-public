import pysus
from pathlib import Path

PROCESSED_DIR = Path("data/processed/datasus")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

UF = "SP"

def testar_pysus():
    print("Testando pySUS v2.3.0...")

    # Testa SIH
    try:
        arquivos = pysus.sih.list_files(UF, year=2023, month=1)
        print(f"SIH disponível — arquivos: {len(arquivos)}")
        for a in arquivos[:3]:
            print(f"  {a}")
    except Exception as e:
        print(f"Erro SIH: {e}")

    # Testa SIM
    try:
        arquivos = pysus.sim.list_files(UF, year=2022)
        print(f"\nSIM disponível — arquivos: {len(arquivos)}")
        for a in arquivos[:3]:
            print(f"  {a}")
    except Exception as e:
        print(f"Erro SIM: {e}")

    # Testa SINASC
    try:
        arquivos = pysus.sinasc.list_files(UF, year=2022)
        print(f"\nSINASC disponível — arquivos: {len(arquivos)}")
        for a in arquivos[:3]:
            print(f"  {a}")
    except Exception as e:
        print(f"Erro SINASC: {e}")

if __name__ == "__main__":
    testar_pysus()