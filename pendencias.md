# Pendências Técnicas

Registro de ajustes e melhorias identificadas ao longo do desenvolvimento.

---

## Em aberto

### [P002] API SICONFI indisponível para municípios
- **Onde:** `collectors/siconfi/coletor.py`
- **Problema:** endpoint `/rreo` retorna vazio para Ferraz de Vasconcelos via API REST
- **Solução adotada:** download manual dos CSVs FINBRA pelo portal do SICONFI
- **Ação futura:** monitorar se a API volta a funcionar; tentar endpoint `/dca`
- **Prioridade:** baixa

### [P006] Emendas parlamentares — sem filtro por município na API
- **Onde:** `collectors/portal_federal/coletor_emendas.py`
- **Problema:** endpoint `/api-de-dados/emendas` não possui parâmetro de município
- **Dados coletados incorretos:** arquivo `emendas_ferraz.csv` contém dados de outros estados
- **Solução futura (opção A):** cruzar via `/api-de-dados/emendas/documentos/{codigo}`
  usando os códigos de emenda dos convênios já coletados
- **Solução futura (opção B):** baixar CSV completo do Conjunto de Dados do Portal
  Federal e filtrar por município localmente
- **Prioridade:** média — fase de cruzamentos

### [P008] Investigar dispensas de licitação — consultoria
- **Onde:** `data/processed/tce_sp/licitacoes_ferraz.csv`
- **Status parcial:** fracionamento ✅ · locações ✅ · medicamentos ✅
- **Pendente:** investigar 4 dispensas de consultoria identificadas
- **Prioridade:** baixa

### [P012] Investigar aditivos contratuais DATACITY
- **Onde:** `data/processed/tce_sp/datacity_analise.csv`
- **Achado:** Contrato 161/2016 ativo por pelo menos 4 anos com múltiplos aditivos (até 9º)
- **Ação:** solicitar via LAI os contratos com todos os termos aditivos e verificar
  se respeitaram o limite de 25% do valor original (Lei 8.666/93)
- **Prioridade:** alta

### [P013] Verificar classificação do concreto usinado — CASAMAX
- **Onde:** `data/processed/tce_sp/ajustes_ferraz.csv`
- **Achado:** R$ 9,1mi em concreto usinado (CBUQ) classificado como "material de consumo"
  em 8 contratos separados — possível fracionamento e classificação indevida
- **Ação:** solicitar via LAI os processos licitatórios e verificar preços vs mercado regional
- **Prioridade:** alta

---

## Resolvidas

| ID | Descrição | Sessão |
|---|---|---|
| P001 | Padronização de separador nos CSVs processados | Sessão 2 |
| P003 | Código IBGE incorreto (3515103 → 3515707) | Sessão 1 |
| P004 | Critério de totalização de despesas (Liquidadas) | Sessão 2 |
| P005 | Parâmetros corretos do endpoint de convênios | Sessão 3 |
| P007 | Encoding incorreto nos nomes de colunas — licitações TCE-SP | Sessão 5 |
| P009 | Monitorar pessoal e saúde — incluído no dashboard AUDESP | Sessão 6 |
| P010 | Empresa baixada (E DE SOUZA LOPES) — baixa posterior aos contratos | Sessão 7 |
| P011 | Custo mensal nas locações de imóveis | Sessão 8 |
---

## Formato de registro

```
### [PXXX] Título curto
- **Onde:** arquivo ou módulo afetado
- **Problema:** descrição do problema
- **Solução:** o que fazer
- **Prioridade:** alta / média / baixa
```