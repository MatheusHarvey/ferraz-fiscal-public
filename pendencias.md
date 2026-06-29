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

### [P014] Dashboard — integrar dados do portal de Ferraz
- **Onde:** `dashboard/app.py`
- **Pendente:** adicionar página com CASAMAX/DATACITY do portal municipal
- **Prioridade:** média

### [P016] Contrato 189/2021 DATACITY — 2º aditivo não localizado
- **Onde:** `data/raw/transparencia_ferraz/datacity/pdfs-complementares/SIAM_189_2021/`
- **Problema:** 2º aditivo não encontrado nos documentos públicos disponíveis
- **Ação:** solicitar via LAI ou verificar se foi publicado posteriormente
- **Prioridade:** baixa

### [P017] Contratos de luminárias DATACITY — RESOLVIDO ✅
- **Onde:** contratos 243/2020 e 111/2021
- **Problema:** dois contratos de objeto similar em anos consecutivos para o mesmo fornecedor
- **Ação:** verificar se houve novo processo licitatório ou substituição irregular
- **Prioridade:** baixa

---

## Resolvidas

| ID | Descrição | Sessão |
|---|---|---|
| P001 | Padronização de separador nos CSVs processados | Sessão 2 |
| P003 | Código IBGE incorreto (3515103 → 3515707) | Sessão 1 |
| P004 | Critério de totalização de despesas (Liquidadas) | Sessão 2 |
| P005 | Parâmetros corretos do endpoint de convênios | Sessão 3 |
| P006 | Emendas federais — R$ 58,6mi extraídos e documentados | Sessão 12 |
| P007 | Encoding incorreto nos nomes de colunas — licitações TCE-SP | Sessão 5 |
| P008 | Empresa baixada (E DE SOUZA LOPES) — baixa posterior aos contratos | Sessão 7 |
| P009 | Monitorar pessoal e saúde — incluído no dashboard AUDESP | Sessão 6 |
| P010 | Custo mensal nas locações de imóveis | Sessão 8 |
| P011 | Portal da Transparência de Ferraz — explorado e coletado | Sessão 10 |
| P012 | Investigar aditivos contratuais DATACITY — PDFs analisados | Sessão 12 |
| P015 | Resumo executivo TCE-SP gerado com autoria | Sessão 12 |
| P013 | Classificação indevida CASAMAX — documentado e consolidado no relatório | Sessão 12 |
| P008 | Dispensas de consultoria — 1 contrato FIA/USP R$ 397k, sem irregularidade | Sessão 12 |
## Formato de registro

```
### [PXXX] Título curto
- **Onde:** arquivo ou módulo afetado
- **Problema:** descrição do problema
- **Solução:** o que fazer
- **Prioridade:** alta / média / baixa
```