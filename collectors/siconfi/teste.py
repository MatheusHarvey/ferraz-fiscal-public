import requests
import json

# Teste com o parâmetro correto: id_ente em vez de co_municipio
r = requests.get(
    "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo",
    params={
        "id_ente": "3515707",
        "an_exercicio": 2023,
        "nr_periodo": 6,
        "limit": 5000,
    }
)

d = r.json()
print(f"Registros encontrados: {d['count']}")

if d["items"]:
    print("\nCampos disponíveis:")
    print(list(d["items"][0].keys()))
    print("\nPrimeiro registro:")
    print(json.dumps(d["items"][0], indent=2))
else:
    print("Sem dados para este período.")
    print("Tentando 2022...")
    
    r2 = requests.get(
        "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo",
        params={
            "id_ente": "3515707",
            "an_exercicio": 2022,
            "nr_periodo": 6,
            "limit": 5000,
        }
    )
    d2 = r2.json()
    print(f"Registros 2022: {d2['count']}")
    if d2["items"]:
        print(json.dumps(d2["items"][0], indent=2))