# Relatório de Indícios de Irregularidade
**Município:** Ferraz de Vasconcelos — SP
**Período analisado:** 2020–2026
**Data do relatório:** 28/06/2026
**Elaborado por:** Matheus Harvey
**Metodologia:** Análise de dados públicos com suporte de ferramentas de inteligência artificial e processamento automatizado de dados.
**Fontes:** TCE-SP · SICONFI/STN · Portal da Transparência Federal · Portal da Transparência Municipal · IBGE · DATASUS · SINAPI/CEF · Receita Federal

---

## 1. Contexto

Este relatório foi gerado pelo Ferraz Fiscal, ferramenta local de auditoria cívica das finanças públicas de Ferraz de Vasconcelos — SP (IBGE: 3515707 | CNPJ: 46.523.197/0001-44). Os dados foram obtidos de fontes públicas oficiais e cruzados com referências técnicas de preços e legislação vigente.

**Contexto socioeconômico:**

| Indicador | Valor | Ano |
|---|---|---|
| População | 179.198 habitantes | Censo 2022 |
| População estimada | 186.479 habitantes | 2025 |
| PIB per capita | R$ 30.826,13 | 2023 |
| IDHM | 0,738 | 2010 |
| Salário médio formal | 2,5 salários mínimos | 2023 |
| Pop. até ½ salário mínimo | 37% | 2010 |
| Urbanização de vias públicas | 11,8% | 2010 |
| Transferências correntes | 70,5% da receita | 2024 |
| Receita total | R$ 732.618.633,68 | 2024 |

---

## 2. Metodologia

Foram analisados dados financeiros do município de 2020 a 2026, obtidos de:
- **TCE-SP/SAGRES:** licitações, dispensas, ajustes e despesas (2014–2025)
- **SICONFI/STN:** receitas e despesas orçamentárias (2021–2025)
- **Portal da Transparência Federal:** convênios e emendas parlamentares
- **Portal da Transparência Municipal:** contratos, compras por itens e emendas
- **SINAPI/CEF:** referência de preços para insumos e composições de obras
- **IBGE e DATASUS:** indicadores socioeconômicos e de saúde

Os dados foram processados com scripts Python e cruzados automaticamente para identificar padrões de irregularidade. Todas as fontes são públicas e verificáveis.

---

## 3. Visão Geral dos Achados

| # | Categoria | Valor | Gravidade |
|---|---|---|---|
| 1 | Classificação indevida CASAMAX — CBUQ como material de consumo | R$ 24.870.992,00 | 🔴 Crítico |
| 2 | DATACITY — aditivos sucessivos e pagamentos sem contrato | R$ 46.930.449,07 | 🔴 Alto |
| 3 | Fracionamento de despesa | R$ 899.781,55 | 🟠 Médio |
| 4 | Locações de imóveis com indícios de direcionamento | R$ 2.776.189,50 | 🟠 Médio |
| 5 | Convênio federal inadimplente | R$ 250.000,00 | 🟡 Baixo |
| **Total investigado** | | **R$ 75.727.412,12** | |

---

## 4. CASAMAX COMERCIAL E SERVIÇOS LTDA

**CNPJ:** 08.183.516/0001-20 · **Município:** Ferraz de Vasconcelos/SP · **Atividade:** Administração de obras

### 4.1 Visão geral dos gastos

| Ano | Valor Empenhado |
|---|---|
| 2020 | R$ 4.452.672,40 |
| 2021 | R$ 4.766.256,06 |
| 2022 | R$ 34.520.040,70 |
| 2023 | R$ 32.049.640,77 |
| 2024 | R$ 7.610.331,31 |
| 2025 | R$ 4.101.555,93 |
| **Total** | **R$ 87.500.497,17** |

**Composição por elemento de despesa:**

| Elemento | Valor | % |
|---|---|---|
| Obras em andamento | R$ 62.110.212,73 | 71% |
| Outros materiais de consumo (CBUQ) | R$ 15.687.625,84 | 18% |
| Obras e instalações | R$ 8.457.251,85 | 10% |
| Outros | R$ 1.244.406,75 | 1% |

### 4.2 Classificação indevida de insumo de obra — Indício principal

Concreto Betuminoso Usinado a Quente (CBUQ), insumo de obra, foi licitado
sistematicamente como "Outros materiais de consumo", inclusive no mesmo
pregão que café, açúcar e biscoitos.

**🔴 Pregão Eletrônico 00030/2026 — Processo 4270**

| Item | Unidade | Quantidade | Preço Unit. | Total | Vencedor |
|---|---|---|---|---|---|
| Açúcar refinado 1kg | UN | 3.750 | R$ 4,00 | R$ 15.000,00 | Nutricionale |
| Biscoito cream cracker 200g | PCT | 1.013 | R$ 2,50 | R$ 2.532,50 | Nutricionale |
| Café torrado 500g | UN | 1.170 | R$ 17,68 | R$ 20.685,60 | Orion |
| **Concreto Asfáltico Faixa V** | **T** | **8.000** | **R$ 648,00** | **R$ 5.184.000,00** | **CASAMAX** |
| **Concreto Asfáltico Faixa IV** | **T** | **8.000** | **R$ 640,00** | **R$ 5.120.000,00** | **CASAMAX** |
| **Material Betuminoso Reciclado** | **T** | **5.000** | **R$ 290,00** | **R$ 1.450.000,00** | **CASAMAX** |

**Total CASAMAX neste pregão: R$ 11.754.000,00**

### 4.3 Análise de preços por processo licitatório

| Processo | Produto | Qtd (t) | Preço/t | Total | vs SINAPI* |
|---|---|---|---|---|---|
| 00032 (11697) | CBUQ Faixa III e IV | 14.000 | R$ 498,00 | R$ 6.972.000 | ✅ dentro |
| 00059 (13846) | CBUQ Faixa III e IV | 11.200 | R$ 548,66 | R$ 6.144.992 | ⚠️ +9,7% |
| 00030 (4270) | Concreto Asfáltico Faixa IV e V | 16.000 | R$ 640–648 | R$ 10.304.000 | 🔴 +28% |
| 00030 (4270) | Material Betuminoso Reciclado | 5.000 | R$ 290,00 | R$ 1.450.000 | — |

*Referência SINAPI SP jun/2022: R$ 500,25/t para CBUQ Faixa C CAP 30/45

**Total CASAMAX nos processos analisados: R$ 24.870.992,00**

**Escalada de preços:** R$ 498/t → R$ 548/t → R$ 648/t (+30% entre processos)

### 4.4 Referência SINAPI para CBUQ — São Paulo

| Período | CBUQ Faixa C CAP 30/45 | CBUQ Faixa C CAP 50/70 | CBUQ Binder |
|---|---|---|---|
| Jun/2022 | R$ 500,25/t | R$ 510,00/t | R$ 447,18/t |
| Dez/2022 | R$ 513,98/t | R$ 524,00/t | R$ 459,46/t |
| Jun/2023 | R$ 490,44/t | R$ 500,00/t | R$ 438,42/t |
| Dez/2023 | R$ 502,70/t | R$ 512,50/t | R$ 449,38/t |

### 4.5 Indícios consolidados

1. **Classificação indevida confirmada** — CBUQ licitado como "material de consumo" em todos os processos analisados, contrariando o art. 6º, XXI e XXII da Lei 14.133/2021
2. **Pregão 00030/2026** — concreto asfáltico no mesmo pregão que café e biscoitos
3. **Preço 28% acima do SINAPI** — processo 00030 pratica R$ 640–648/t vs R$ 500/t de referência
4. **8 contratos separados** de concreto usinado (R$ 9.184.067,46) — possível fracionamento
5. **Concentração de fornecimento** — CASAMAX venceu 100% dos lotes de material asfáltico
6. **Total empenhado 2020–2025:** R$ 87.500.497,17

---

## 5. DATACITY SERVIÇOS LTDA

**CNPJ:** 02.679.522/0001-97 · **Município:** Suzano/SP · **Email:** datacityservicos@gmail.com
**Atividade declarada:** Outras atividades de serviços (CNAE genérico)

### 5.1 Visão geral dos gastos

| Ano | Valor Empenhado |
|---|---|
| 2020 | R$ 4.729.113,05 |
| 2021 | R$ 5.922.737,31 |
| 2022 | R$ 5.658.110,87 |
| 2023 | R$ 5.883.171,07 |
| 2024 | R$ 11.534.578,06 |
| 2025 | R$ 13.202.738,71 |
| **Total** | **R$ 46.930.449,07** |

### 5.2 Contratos identificados

| Contrato | Ano | Objeto | Valor Original |
|---|---|---|---|
| 161/2016 | 2016 | Monitoramento de tráfego (radares) | não localizado |
| 243/2020 | 2020 | Luminárias públicas LED | R$ 1.964.132,00 |
| 111/2021 | 2021 | Luminárias de LED | R$ 1.479.545,04 |
| 189/2021 | 2021 | Apoio técnico e manutenção de rede | R$ 1.164.000,00 |
| 329/2022 | 2022 | Monitoramento e fiscalização viária | R$ 3.540.000,00 |

### 5.3 Aditivos contratuais — Contrato 329/2022

| Instrumento | Vigência | Valor |
|---|---|---|
| Contrato original | 31/08/2022 a 31/08/2023 | R$ 3.540.000,00 |
| 1º Aditivo | 30/08/2023 a 30/08/2024 | R$ 3.845.873,21 |
| 2º Aditivo | 31/08/2024 a 30/08/2025 | R$ 4.008.420,38 |
| 3º Aditivo | 31/08/2025 a 30/08/2026 | R$ 4.230.075,24 |
| **Total acumulado** | **4 anos** | **R$ 15.624.368,83** |

### 5.4 Aditivos contratuais — Contrato 189/2021

| Instrumento | Vigência | Valor |
|---|---|---|
| Contrato original | 25/08/2021 a 25/08/2022 | R$ 1.164.000,00 |
| 1º Aditivo | 25/08/2022 a 24/08/2023 | não localizado |
| 3º Aditivo | 25/08/2023 a 24/08/2024 | R$ 1.503.224,73 |
| 4º Aditivo | 25/08/2024 a 24/08/2025 | R$ 1.570.843,44 |
| 5º Aditivo | 25/08/2025 a 24/08/2026 | R$ 1.654.407,60 |
| **Total parcial** | **5 anos** | **R$ 5.892.475,77** |



### 5.6 Contratos de luminárias — sobreposição de vigência

Os contratos 243/2020 e 111/2021, ambos para fornecimento e
instalação de luminárias públicas LED, apresentam sobreposição
de vigência de aproximadamente 40 dias:

| Contrato | Vigência | Valor |
|---|---|---|
| 243/2020 | 04/11/2020 a 03/08/2021 | R$ 1.964.132,00 |
| 111/2021 | 23/06/2021 a 22/06/2022 | R$ 1.479.545,04 |
| **Total** | | **R$ 3.443.677,04** |

**Sobreposição:** 23/06/2021 a 03/08/2021 (~40 dias)

**Indícios:**
- Objeto idêntico para o mesmo fornecedor em contratos consecutivos
- Ambos derivam do mesmo processo administrativo (G00028)
- Município pagou dois contratos simultâneos para o mesmo serviço
- Possível divisão irregular de contrato ou aditivo registrado como novo contrato

### 5.5 Indícios consolidados

1. **Contrato 161/2016 ativo por 6+ anos** — 4º aditivo em 2020 e 9º em 2022, violando o limite de 5 anos (Lei 14.133/2021, Art. 106)
2. **R$ 43,6 milhões em 65 empenhos sem referência contratual** — pagamentos sem indicação do contrato nos históricos de empenho
3. **Crescimento de 140% em 2025** — novo objeto "Gerenciamento de Soluções Tecnológicas" sem licitação específica identificada
4. **R$ 1.610.915,87 em indenizações e termos de ajuste** — regularizações retroativas de pagamentos
5. **Reajustes acumulados:** +19,5% no contrato 329/2022 e +42% no 189/2021
6. **2º aditivo do contrato 189/2021 não localizado** nos documentos públicos disponíveis
7. **Email Gmail como contato comercial** — empresa que fatura R$ 13mi/ano com o município usa conta gratuita

---

## 6. Fracionamento de Despesa

Fornecedores com múltiplos contratos por dispensa no mesmo ano cujos valores somados ultrapassam o limite legal de R$ 50.000, caracterizando possível fracionamento vedado pelo Art. 20 da Lei 14.133/2021.

**Total: R$ 899.781,55 | 10 casos | concentrados em 2024**

| Empresa | Ano | Contratos | Valor Total | Observação |
|---|---|---|---|---|
| BERTY CONSTRUÇÕES LTDA EPP | 2024 | 7x | R$ 150.227,40 | — |
| RT LOCAÇÕES DE MÁQUINAS E EQUIPAMENTOS | 2024 | 3x | R$ 109.850,84 | — |
| E DE SOUZA LOPES | 2024 | 4x | R$ 102.149,49 | Empresa baixada ago/2025 |
| THREE F ENGENHARIA E CONSULTORIA | 2024 | 5x | R$ 93.250,12 | — |
| DRA LTDA | 2024 | 3x | R$ 86.150,84 | — |
| W & MACEDO ELÉTRICA EIRELI | 2024 | 4x | R$ 83.807,77 | CNAE varejista — obra de eng. |
| FABIO BRETAS MAIA | 2024 | 3x | R$ 74.120,74 | — |
| JA RODRIGUES ARQUITETURA | 2024 | 2x | R$ 69.940,89 | Aberta jul/2024, já contratada |
| TEC-CONST EMPREENDIMENTOS | 2022 | 2x | R$ 65.816,01 | Empresa inapta desde mai/2026 |
| CARLOS ALEXANDRO DE O. ARRUDA | 2024 | 2x | R$ 64.467,45 | CNAE transportes — obra de eng. |

---

## 7. Locações de Imóveis por Dispensa

**19 contratos · R$ 2.776.189,50 · 87% com pessoas físicas**

### 7.1 Indícios de direcionamento familiar

| Contratados | Sobrenome | Data | Valor Total |
|---|---|---|---|
| BRAULIO BUENO DE ALMEIDA + SILVANA VALIERIS BUENO DE ALMEIDA | ALMEIDA | 19/04/2021 | R$ 450.000,00 |
| SILVIO FRANCISCO CHAGAS + REGINA CLAUDINA DA CUNHA CHAGAS | CHAGAS | 20/05/2022 | R$ 222.015,90 |

Mesmo sobrenome composto, contratos com valores idênticos firmados na mesma data.

### 7.2 Maiores contratos por custo mensal

| Contratado | Valor Total | Vigência | Custo Mensal |
|---|---|---|---|
| INDÚSTRIA E COMÉRCIO DE ALUMÍNIO ABC LTDA | R$ 464.583,00 | sem datas | s/d |
| LATUF CURY PARTICIPAÇÕES S.A | R$ 360.000,00 | jun/2021 a dez/2023 | R$ 12.000,00/mês |
| ROSA MARIA PINHEIRO ABISSAMRA | R$ 234.000,00 | jun/2022 a dez/2024 | R$ 7.800,00/mês |
| BRAULIO BUENO DE ALMEIDA | R$ 225.000,00 | abr/2021 a out/2023 | R$ 7.500,00/mês |
| SILVANA VALIERIS BUENO DE ALMEIDA | R$ 225.000,00 | abr/2021 a out/2023 | R$ 7.500,00/mês |

**Nota:** INDÚSTRIA E COMÉRCIO DE ALUMÍNIO ABC LTDA — maior contrato de locação (R$ 464.583,00) sem datas de vigência registradas.

### 7.3 Todos os contratos

| Contratado | Valor Total | Custo Mensal |
|---|---|---|
| INDÚSTRIA E COMÉRCIO DE ALUMÍNIO ABC LTDA | R$ 464.583,00 | s/d |
| LATUF CURY PARTICIPAÇÕES S.A | R$ 360.000,00 | R$ 12.000,00/mês |
| ROSA MARIA PINHEIRO ABISSAMRA | R$ 234.000,00 | R$ 7.800,00/mês |
| BRAULIO BUENO DE ALMEIDA | R$ 225.000,00 | R$ 7.500,00/mês |
| ELIZABETE CORREIA SARMENTO | R$ 225.000,00 | R$ 7.500,00/mês |
| SILVANA VALIERIS BUENO DE ALMEIDA | R$ 225.000,00 | R$ 7.500,00/mês |
| EUDAS DE CARVALHO | R$ 210.000,00 | R$ 7.000,00/mês |
| LUCIANO ANDRE DA SILVA | R$ 147.666,60 | R$ 4.922,22/mês |
| ARNALDO DA SILVA ALVES | R$ 135.000,00 | R$ 4.500,00/mês |
| REGINA CLAUDINA DA CUNHA CHAGAS | R$ 111.007,95 | R$ 3.700,26/mês |
| SILVIO FRANCISCO CHAGAS | R$ 111.007,95 | R$ 3.700,26/mês |
| MARIA LUIZA BASTOS DOS SANTOS | R$ 102.000,00 | R$ 3.400,00/mês |
| JOAQUIM APARECIDO DE ATAIDE SILVA SANTOS | R$ 64.500,00 | R$ 2.150,00/mês |
| MARILIA MARTINELLI LOPES RODRIGUES | R$ 48.000,00 | R$ 4.000,00/mês |
| FRANCISCO BARBOSA DE LUNA | R$ 27.000,00 | R$ 900,00/mês |
| VILMA AMERICO | R$ 22.200,00 | R$ 1.850,00/mês |
| GILENO PEREIRA | R$ 22.200,00 | R$ 1.850,00/mês |
| JOSE CARLOS PEREIRA | R$ 21.012,00 | R$ 1.751,00/mês |
| MARIA RITA MASCHIETTO PEREIRA | R$ 21.012,00 | R$ 1.751,00/mês |

---

## 8. Emendas Parlamentares

### 8.1 Emendas federais — 2020–2024

Fonte: Portal da Transparência Federal

| Indicador | Valor |
|---|---|
| Total de registros | 211 |
| Valor total empenhado | R$ 58.605.854,88 |
| Valor total pago | R$ 46.584.417,64 |

**Evolução anual:**

| Ano | Valor Empenhado |
|---|---|
| 2020 | R$ 3.393.648,88 |
| 2021 | R$ 4.241.250,00 |
| 2022 | R$ 2.931.332,00 |
| 2023 | R$ 20.102.299,00 |
| 2024 | R$ 27.937.325,00 |

**Crescimento de 586% em 2023** — coincide com o pico de gastos da CASAMAX (R$ 32mi em 2023).

**Top autores:**

| Parlamentar | Valor Empenhado |
|---|---|
| RODRIGO GAMBALE | R$ 12.020.758,00 |
| COM. DA SAÚDE | R$ 10.323.623,00 |
| COM. DESENV REGIONAL E TURISMO | R$ 5.743.773,00 |
| ALENCAR SANTANA | R$ 5.000.000,00 |
| ABOU ANNI | R$ 4.000.254,00 |

**Ponto de atenção:** RODRIGO GAMBALE é o maior autor de emendas federais
(R$ 12,0mi) e também aparece como destinador de emendas municipais —
atuação em dois níveis de governo para o mesmo município.

**Favorecidos:**

| Favorecido | Valor |
|---|---|
| Fundo Municipal de Saúde | R$ 30.123.685,00 |
| Município de Ferraz de Vasconcelos | R$ 27.970.919,88 |
| Fundo Municipal de Assistência Social | R$ 500.000,00 |

### 8.2 Emendas municipais — 2026

Fonte: Portal da Transparência Municipal

| Indicador | Valor |
|---|---|
| Total de emendas | 172 |
| Valor total orçado | R$ 12.769.178,52 |
| Valor total empenhado | R$ 10.115.200,60 |
| Receita total recebida | R$ 17.669.827,76 |
| Emendas sem empenhamento | 29 (R$ 2.376.126,40) |

**12 emendas com receita recebida maior que o orçado** — R$ 14.020.943,04
recebidos acima do planejamento orçamentário, principalmente via transferências
federais fundo a fundo para saúde (SUS).

---

## 9. Convênios Federais

**1 convênio inadimplente:**
- **V Festival Cultural Raízes (2007):** R$ 250.000,00 recebidos do Ministério do Turismo. Prestação de contas nunca regularizada. Situação: INADIMPLENTE.

**1 inadimplência suspensa:**
- **Equipamentos educação infantil (2006):** R$ 90.090,00 recebidos do FNDE. Situação irregular há quase 20 anos.

---

## 10. Achados sem irregularidade

### 10.1 Dispensas de medicamentos

607 dispensas analisadas (2020–2024). Volume elevado em 2024 concentrado em poucos processos — padrão compatível com reposição semestral de estoque. **Avaliação: gestão adequada.**

### 10.2 Indicadores AUDESP — Limites constitucionais

Gastos com ensino e saúde dentro dos limites constitucionais em 2022–2024. Único alerta em 2016 (pessoal 54,9% > limite 54%) — gestão anterior.

---

## 11. Recomendações

1. **Denunciar ao TCE-SP** o Pregão 00030/2026 — mistura de café e concreto asfáltico no mesmo processo licitatório, com preços 28% acima do SINAPI
2. **Denunciar ao TCE-SP** a classificação sistemática de CBUQ como "material de consumo" em todos os processos da CASAMAX
3. **Investigar** os contratos DATACITY 161/2016 e 189/2021 — vigências que ultrapassam ou atingem o limite legal de 5 anos
4. **Solicitar via LAI** o 2º aditivo do contrato 189/2021 da DATACITY não localizado
5. **Investigar vínculos** entre os pares ALMEIDA e CHAGAS e agentes públicos municipais
6. **Verificar habilitação** de W&MACEDO ELÉTRICA e CARLOS ALEXANDRO nas dispensas de 2024
7. **Apurar fracionamento** em BERTY CONSTRUÇÕES (7 contratos, R$ 150k) e THREE F ENGENHARIA (5 contratos, R$ 93k)
8. **Canal de denúncia TCE-SP:** https://www.tce.sp.gov.br/fale-conosco

---

*Relatório gerado pelo Ferraz Fiscal — ferramenta de auditoria cívica local.
Dados públicos obtidos de fontes oficiais. Este documento não substitui análise jurídica especializada.*
