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

### [P006] Emendas parlamentares federais — sem filtro por município na API
- **Onde:** `collectors/portal_federal/coletor_emendas.py`
- **Problema:** endpoint `/api-de-dados/emendas` não possui parâmetro de município
- **Nota:** emendas municipais já coletadas via portal de Ferraz (172 registros)
- **Pendente:** emendas federais destinadas a Ferraz ainda não coletadas
- **Solução futura:** baixar CSV completo do Portal Federal e filtrar localmente
- **Prioridade:** média

### [P008] Investigar dispensas de licitação — consultoria
- **Onde:** `data/processed/tce_sp/licitacoes_ferraz.csv`
- **Status parcial:** fracionamento ✅ · locações ✅ · medicamentos ✅
- **Pendente:** investigar 4 dispensas de consultoria identificadas
- **Prioridade:** baixa

### [P012] Investigar aditivos contratuais DATACITY
- **Onde:** `data/raw/transparencia_ferraz/datacity/`
- **Achado:** Contrato 161/2016 ativo por pelo menos 6 anos com 9 aditivos
- **PDFs obtidos:** contratos 329/2022, 189/2021, 243/2020, 111/2021 e aditivos
- **Pendente:** ler PDFs e extrair valores originais vs aditivos
- **Pendente:** reconciliar gap de R$ 30mi sem contrato identificado (2020-2023)
- **Prioridade:** alta

### [P013] Classificação indevida de concreto usinado — CASAMAX
- **Onde:** processos 00030, 00032, 00059 — portal transparência Ferraz
- **Achado confirmado:** CBUQ licitado como "material de consumo" em todos os processos
- **Achado confirmado:** Pregão 00030/2026 mistura café, açúcar e biscoito com 21.000t de asfalto
- **Escalada de preços:** R$ 498/t → R$ 548/t → R$ 648/t (aumento de 30%)
- **Desvio SINAPI:** processo 00030 pratica R$ 640-648/t vs R$ 500/t SINAPI (+28%)
- **LAI:** não necessária — dados obtidos via portal de transparência
- **Pendente:** consolidar no relatório final para denúncia TCE-SP
- **Prioridade:** alta

### [P014] Dashboard — integrar dados do portal de Ferraz
- **Onde:** `dashboard/app.py`
- **Pendente:** adicionar página com CASAMAX/DATACITY do portal municipal
- **Prioridade:** média

### [P015] Relatório final — consolidação para denúncia TCE-SP
- **Onde:** `docs/relatorio_irregularidades_20260620.md`
- **Pendente:** resumo executivo de 1 página
- **Pendente:** numerar e consolidar todos os achados
- **Pendente:** definir timing com base nas eleições municipais
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