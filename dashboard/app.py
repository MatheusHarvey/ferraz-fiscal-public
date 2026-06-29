import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Ferraz Fiscal",
    page_icon="🔍",
    layout="wide",
)

st.markdown("""
    <style>
        .titulo { font-size: 2rem; font-weight: 700; color: #1a1a2e; }
        .subtitulo { font-size: 1rem; color: #555; margin-bottom: 2rem; }
        .alerta { background: #fff3f3; border-left: 4px solid #e63946;
                  padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0; }
        .alerta-medio { background: #fff8f0; border-left: 4px solid #f4a261;
                  padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0; }
        .ok { background: #f0fff4; border-left: 4px solid #2d6a4f;
              padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0; }
        .info { background: #f0f4ff; border-left: 4px solid #2196F3;
              padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0; }
    </style>
""", unsafe_allow_html=True)

SICONFI_DIR  = Path("data/processed/siconfi")
TCE_DIR      = Path("data/processed/tce_sp")
PORTAL_DIR   = Path("data/processed/transparencia_ferraz")
ANOS = [2021, 2022, 2023, 2024, 2025]

# ── Funções de carregamento ──────────────────────────────────────────────────

@st.cache_data
def carregar_siconfi(tipo: str) -> pd.DataFrame:
    frames = []
    for ano in ANOS:
        arquivo = SICONFI_DIR / f"{tipo}_{ano}.csv"
        if arquivo.exists():
            df = pd.read_csv(arquivo, sep=";", decimal=",", encoding="utf-8-sig")
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

@st.cache_data
def carregar_tce(nome: str) -> pd.DataFrame:
    caminho = TCE_DIR / nome
    if caminho.exists():
        return pd.read_csv(caminho, sep=";", encoding="utf-8-sig", dtype=str)
    return pd.DataFrame()

@st.cache_data
def carregar_audesp() -> pd.DataFrame:
    caminho = TCE_DIR / "audesp_ferraz.csv"
    if caminho.exists():
        df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig")
        for col in ["Despesa Empenhada Ensino (%)", "Despesa Empenhada Saúde (%)",
                    "Despesa com Pessoal Poder Executivo (%)"]:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(",", ".").str.strip(),
                    errors="coerce"
                )
        return df
    return pd.DataFrame()

@st.cache_data
def carregar_ibge() -> pd.DataFrame:
    caminho = Path("data/processed/ibge/ibge_ferraz.csv")
    if caminho.exists():
        return pd.read_csv(caminho, sep=";", encoding="utf-8-sig")
    return pd.DataFrame()

@st.cache_data
def carregar_portal(nome: str) -> pd.DataFrame:
    caminho = PORTAL_DIR / nome
    if caminho.exists():
        return pd.read_csv(caminho, sep=";", encoding="utf-8-sig", dtype=str)
    return pd.DataFrame()

def formatar_reais(valor: float) -> str:
    return f"R$ {valor/1e6:_.2f} mi".replace(".", ",").replace("_", ".")

# ── Cabeçalho ────────────────────────────────────────────────────────────────

st.markdown('<div class="titulo">🔍 Ferraz Fiscal</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Monitoramento das finanças públicas de Ferraz de Vasconcelos — SP</div>', unsafe_allow_html=True)
st.divider()

# ── Sidebar ──────────────────────────────────────────────────────────────────

st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Seção",
    [
        "📊 Visão Geral",
        "🔴 Fornecedores Investigados",
        "⚠️ Irregularidades",
        "📋 Limites Constitucionais",
        "🏙️ Contexto Socioeconômico",
    ]
)
st.sidebar.divider()
st.sidebar.title("Filtros")
ano_selecionado = st.sidebar.selectbox("Ano", ANOS, index=len(ANOS)-1)

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 — VISÃO GERAL
# ════════════════════════════════════════════════════════════════════════════

if pagina == "📊 Visão Geral":

    receitas        = carregar_siconfi("receitas")
    despesas        = carregar_siconfi("despesas")
    despesas_funcao = carregar_siconfi("despesas_funcao")

    if receitas.empty or despesas.empty:
        st.error("Dados SICONFI não encontrados em data/processed/siconfi/")
        st.stop()

    CONTA_TOTAL_RECEITA = "RECEITAS (EXCETO INTRA-ORÇAMENTÁRIAS) (I)"

    receita_total = receitas[
        (receitas["ano"] == ano_selecionado) &
        (receitas["Conta"] == CONTA_TOTAL_RECEITA)
    ]["Valor"].sum()

    despesas_ano  = despesas[despesas["ano"] == ano_selecionado]
    despesa_total = despesas_ano[
        (despesas_ano["Conta"] == "Total Geral da Despesa") &
        (despesas_ano["Coluna"] == "Despesas Liquidadas")
    ]["Valor"].sum()

    saldo = receita_total - despesa_total

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Receita Total", formatar_reais(receita_total))
    with col2:
        st.metric("Despesa Total", formatar_reais(despesa_total))
    with col3:
        st.metric("Saldo", formatar_reais(saldo), delta=formatar_reais(saldo))

    st.divider()
    st.subheader("Evolução anual — Receitas × Despesas")

    evolucao = []
    for ano in ANOS:
        r = receitas[
            (receitas["ano"] == ano) &
            (receitas["Conta"] == CONTA_TOTAL_RECEITA)
        ]["Valor"].sum()
        d = despesas[
            (despesas["ano"] == ano) &
            (despesas["Conta"] == "Total Geral da Despesa") &
            (despesas["Coluna"] == "Despesas Liquidadas")
        ]["Valor"].sum()
        if r > 0 or d > 0:
            evolucao.append({"Ano": ano, "Receitas": r/1e6, "Despesas": d/1e6})

    if evolucao:
        df_ev = pd.DataFrame(evolucao)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_ev["Ano"], y=df_ev["Receitas"], name="Receitas",
            line=dict(color="#2196F3", width=2),
            hovertemplate="R$ %{y:,.2f} mi<extra>Receitas</extra>"
        ))
        fig.add_trace(go.Scatter(
            x=df_ev["Ano"], y=df_ev["Despesas"], name="Despesas",
            line=dict(color="#e63946", width=2),
            hovertemplate="R$ %{y:,.2f} mi<extra>Despesas</extra>"
        ))
        fig.update_layout(
            xaxis=dict(tickmode="linear", dtick=1),
            yaxis=dict(tickprefix="R$ ", ticksuffix=" mi"),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=10, b=0),
            height=350,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(f"Despesas por área — {ano_selecionado}")

    if not despesas_funcao.empty:
        df_func = despesas_funcao[
            (despesas_funcao["ano"] == ano_selecionado) &
            (despesas_funcao["Coluna"].str.contains("Empenhadas", na=False)) &
            (despesas_funcao["Conta"].str.match(r"^\d{2} -", na=False))
        ].copy()

        if not df_func.empty:
            df_func = df_func.groupby("Conta")["Valor"].sum().sort_values(ascending=True)
            df_func.index = df_func.index.str.replace(r"^\d{2} - ", "", regex=True)
            fig2 = go.Figure(go.Bar(
                x=df_func.values / 1e6, y=df_func.index,
                orientation="h", marker_color="#2196F3",
                hovertemplate="R$ %{x:,.2f} mi<extra></extra>"
            ))
            fig2.update_layout(
                xaxis=dict(tickprefix="R$ ", ticksuffix=" mi"),
                margin=dict(l=0, r=0, t=10, b=0), height=400,
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("Valores em milhões de R$")

    st.divider()
    st.caption("Fonte: SICONFI / Secretaria do Tesouro Nacional · Dados: 2021–2025")

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 — FORNECEDORES INVESTIGADOS
# ════════════════════════════════════════════════════════════════════════════

elif pagina == "🔴 Fornecedores Investigados":

    st.subheader("🔴 Fornecedores Investigados")
    st.caption("Fontes: TCE-SP · Portal da Transparência Municipal · SINAPI/CEF · Dados: 2020–2026")

    # Resumo executivo
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CASAMAX — total empenhado", "R$ 87,5 mi",
                  delta="2020–2025", delta_color="inverse")
    with col2:
        st.metric("DATACITY — total empenhado", "R$ 46,9 mi",
                  delta="2020–2025", delta_color="inverse")
    with col3:
        st.metric("Desvio SINAPI — CBUQ 2026", "+28%",
                  delta="R$ 648/t vs R$ 500/t", delta_color="inverse")
    with col4:
        st.metric("Aditivos DATACITY", "9 aditivos",
                  delta="Contrato de 2016 ainda vigente", delta_color="inverse")

    st.divider()

    # ── CASAMAX ──
    st.subheader("🏗️ CASAMAX COMERCIAL E SERVIÇOS LTDA")
    st.caption("CNPJ: 08.183.516/0001-20 · Ferraz de Vasconcelos/SP · Pavimentação asfáltica")

    # Evolução anual CASAMAX
    casamax_anos = pd.DataFrame([
        {"Ano": 2020, "Valor": 4452672.40},
        {"Ano": 2021, "Valor": 4766256.06},
        {"Ano": 2022, "Valor": 34520040.70},
        {"Ano": 2023, "Valor": 32049640.77},
        {"Ano": 2024, "Valor": 7610331.31},
        {"Ano": 2025, "Valor": 4101555.93},
    ])

    col1, col2 = st.columns(2)

    with col1:
        fig_cas = go.Figure(go.Bar(
            x=casamax_anos["Ano"],
            y=casamax_anos["Valor"] / 1e6,
            marker_color=["#e63946" if v > 20 else "#f4a261"
                          for v in casamax_anos["Valor"] / 1e6],
            hovertemplate="R$ %{y:,.2f} mi<extra></extra>",
        ))
        fig_cas.update_layout(
            title="Evolução anual de empenhos (R$ mi)",
            xaxis=dict(tickmode="linear", dtick=1),
            yaxis=dict(tickprefix="R$ ", ticksuffix=" mi"),
            margin=dict(l=0, r=0, t=30, b=0),
            height=300,
        )
        st.plotly_chart(fig_cas, use_container_width=True)

    with col2:
        # Composição por elemento
        elementos = pd.DataFrame([
            {"Elemento": "Obras em andamento", "Valor": 62110212.73, "Pct": 71},
            {"Elemento": "Materiais de consumo (CBUQ)", "Valor": 15687625.84, "Pct": 18},
            {"Elemento": "Obras e instalações", "Valor": 8457251.85, "Pct": 10},
            {"Elemento": "Outros", "Valor": 1244406.75, "Pct": 1},
        ])
        fig_pie = go.Figure(go.Pie(
            labels=elementos["Elemento"],
            values=elementos["Valor"],
            hole=0.4,
            marker_colors=["#e63946", "#f4a261", "#2196F3", "#aaa"],
        ))
        fig_pie.update_layout(
            title="Composição dos gastos",
            margin=dict(l=0, r=0, t=30, b=0),
            height=300,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Análise de preços
    st.subheader("Análise de preços por processo licitatório")

    precos = pd.DataFrame([
        {"Processo": "00032 (11697)", "Produto": "CBUQ Faixa III e IV",
         "Qtd_t": 14000, "Preco_t": 498.00, "Total": 6972000, "vs_SINAPI": "✅ ok"},
        {"Processo": "00059 (13846)", "Produto": "CBUQ Faixa III e IV",
         "Qtd_t": 11200, "Preco_t": 548.66, "Total": 6144992, "vs_SINAPI": "⚠️ +9,7%"},
        {"Processo": "00030 (4270)", "Produto": "Concreto Asfáltico Faixa IV e V",
         "Qtd_t": 16000, "Preco_t": 644.00, "Total": 10304000, "vs_SINAPI": "🔴 +28%"},
        {"Processo": "00030 (4270)", "Produto": "Material Betuminoso Reciclado",
         "Qtd_t": 5000, "Preco_t": 290.00, "Total": 1450000, "vs_SINAPI": "—"},
    ])

    col1, col2 = st.columns(2)
    with col1:
        fig_preco = go.Figure(go.Bar(
            x=["R$ 498/t", "R$ 548/t", "R$ 648/t"],
            y=[498, 548, 648],
            marker_color=["#2196F3", "#f4a261", "#e63946"],
            text=["Proc. 00032", "Proc. 00059", "Proc. 00030"],
            textposition="outside",
            hovertemplate="%{y:,.0f} R$/t<extra></extra>",
        ))
        fig_preco.add_hline(y=500.25, line_dash="dash", line_color="gray",
                           annotation_text="SINAPI jun/2022: R$ 500,25/t")
        fig_preco.update_layout(
            title="Escalada de preços do CBUQ",
            yaxis=dict(tickprefix="R$ ", ticksuffix="/t"),
            margin=dict(l=0, r=0, t=30, b=0),
            height=300,
        )
        st.plotly_chart(fig_preco, use_container_width=True)

    with col2:
        st.dataframe(
            precos[["Processo", "Produto", "Qtd_t", "Preco_t", "vs_SINAPI"]].rename(columns={
                "Qtd_t": "Qtd (t)", "Preco_t": "R$/t", "vs_SINAPI": "vs SINAPI"
            }),
            use_container_width=True, hide_index=True
        )
        st.metric("Total nos 4 processos", "R$ 24.870.992,00")

    st.markdown("""
    <div class="alerta">
    🔴 <strong>Pregão 00030/2026 — Achado crítico:</strong> concreto asfáltico (8.000t + 8.000t)
    e material betuminoso (5.000t) licitados no <strong>mesmo pregão</strong> que café, açúcar e biscoitos,
    todos classificados como "material de consumo". Preço praticado: R$ 640–648/t vs R$ 500/t SINAPI
    (<strong>+28%</strong>). Total CASAMAX neste pregão: <strong>R$ 11.754.000,00</strong>.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── DATACITY ──
    st.subheader("📡 DATACITY SERVIÇOS LTDA")
    st.caption("CNPJ: 02.679.522/0001-97 · Suzano/SP · Email: datacityservicos@gmail.com")

    datacity_anos = pd.DataFrame([
        {"Ano": 2020, "Valor": 4729113.05},
        {"Ano": 2021, "Valor": 5922737.31},
        {"Ano": 2022, "Valor": 5658110.87},
        {"Ano": 2023, "Valor": 5883171.07},
        {"Ano": 2024, "Valor": 11534578.06},
        {"Ano": 2025, "Valor": 13202738.71},
    ])

    col1, col2 = st.columns(2)

    with col1:
        fig_dat = go.Figure(go.Bar(
            x=datacity_anos["Ano"],
            y=datacity_anos["Valor"] / 1e6,
            marker_color=["#e63946" if v > 10 else "#f4a261"
                          for v in datacity_anos["Valor"] / 1e6],
            hovertemplate="R$ %{y:,.2f} mi<extra></extra>",
        ))
        fig_dat.add_hline(y=5.5, line_dash="dash", line_color="gray",
                          annotation_text="Média histórica R$ 5,5mi")
        fig_dat.update_layout(
            title="Evolução anual de empenhos (R$ mi)",
            xaxis=dict(tickmode="linear", dtick=1),
            yaxis=dict(tickprefix="R$ ", ticksuffix=" mi"),
            margin=dict(l=0, r=0, t=30, b=0),
            height=300,
        )
        st.plotly_chart(fig_dat, use_container_width=True)

    with col2:
        # Aditivos contratos
        aditivos = pd.DataFrame([
            {"Instrumento": "Contrato 329/2022", "Vigência": "ago/22–ago/23", "Valor": 3540000},
            {"Instrumento": "1º Aditivo", "Vigência": "ago/23–ago/24", "Valor": 3845873.21},
            {"Instrumento": "2º Aditivo", "Vigência": "ago/24–ago/25", "Valor": 4008420.38},
            {"Instrumento": "3º Aditivo", "Vigência": "ago/25–ago/26", "Valor": 4230075.24},
        ])
        fig_adt = go.Figure(go.Bar(
            x=aditivos["Instrumento"],
            y=aditivos["Valor"] / 1e6,
            marker_color=["#2196F3", "#f4a261", "#f4a261", "#e63946"],
            hovertemplate="R$ %{y:,.2f} mi<extra></extra>",
            text=[f"R$ {v/1e6:,.1f}mi" for v in aditivos["Valor"]],
            textposition="outside",
        ))
        fig_adt.update_layout(
            title="Contrato 329/2022 — Evolução com aditivos",
            yaxis=dict(tickprefix="R$ ", ticksuffix=" mi"),
            margin=dict(l=0, r=0, t=30, b=0),
            height=300,
        )
        st.plotly_chart(fig_adt, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Contrato 329/2022 — total acumulado",
                  "R$ 15.624.368,83", delta="4 anos via aditivos")
    with col2:
        st.metric("Contrato 189/2021 — total parcial",
                  "R$ 5.892.475,77", delta="5 anos via aditivos")
    with col3:
        st.metric("Empenhos sem contrato identificado",
                  "65 empenhos", delta="R$ 43,6 mi sem referência", delta_color="inverse")

    st.markdown("""
    <div class="alerta">
    🔴 <strong>Contrato 161/2016 ativo por 6+ anos</strong> — o 4º aditivo aparece em 2020
    e o 9º em 2022, violando o limite de 5 anos (Lei 14.133/2021, Art. 106).<br>
    🔴 <strong>R$ 43,6 milhões em 65 empenhos</strong> sem referência contratual clara nos
    históricos de empenho — impossível rastrear qual contrato ampara cada pagamento.<br>
    ⚠️ <strong>Crescimento de +140% em 2025</strong> — novo objeto "Soluções Tecnológicas
    Integradas" sem licitação específica identificada.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("Fonte: TCE-SP · Portal da Transparência Municipal · SINAPI/CEF · Dados: 2020–2026")

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 — IRREGULARIDADES
# ════════════════════════════════════════════════════════════════════════════

elif pagina == "⚠️ Irregularidades":

    st.subheader("⚠️ Irregularidades — Dispensas e Contratos Suspeitos")
    st.caption("Fonte: Portal da Transparência Municipal do TCE-SP · Dados: 2021–2024")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Casos de fracionamento", "10",
                  delta="R$ 899,7 mil", delta_color="inverse")
    with col2:
        st.metric("Locações suspeitas", "19",
                  delta="R$ 2,77 mi", delta_color="inverse")
    with col3:
        st.metric("Total investigado", "R$ 3,67 mi",
                  delta="em dispensas", delta_color="inverse")

    st.divider()

    # ── Fracionamento ──
    st.subheader("Fracionamento de despesa")
    frac = carregar_tce("suspeitos_fracionamento.csv")

    if not frac.empty:
        frac["valor_total"] = pd.to_numeric(frac["valor_total"], errors="coerce")
        frac["qtd_contratos"] = pd.to_numeric(frac["qtd_contratos"], errors="coerce")

        fig_frac = go.Figure(go.Bar(
            x=frac.sort_values("valor_total")["valor_total"] / 1e3,
            y=frac.sort_values("valor_total")["Nome da empresa contratada"],
            orientation="h",
            marker_color="#e63946",
            text=frac.sort_values("valor_total")["qtd_contratos"].astype(int).astype(str) + "x",
            textposition="outside",
            hovertemplate="R$ %{x:,.1f} mil<extra></extra>",
        ))
        fig_frac.update_layout(
            xaxis=dict(tickprefix="R$ ", ticksuffix=" mil"),
            margin=dict(l=0, r=60, t=10, b=0),
            height=380,
        )
        st.plotly_chart(fig_frac, use_container_width=True)
        st.caption("Números nas barras indicam quantidade de contratos por dispensa no mesmo ano.")

        st.markdown("""
        <div class="alerta">
        🔴 <strong>E DE SOUZA LOPES</strong> — empresa com situação BAIXADA na Receita Federal
        (ago/2025, após os contratos de 2024).<br>
        ⚠️ <strong>W & MACEDO ELÉTRICA</strong> — CNAE de comércio varejista, contratada para
        obras de engenharia.<br>
        ⚠️ <strong>JA RODRIGUES ARQUITETURA</strong> — empresa aberta em jul/2024 e já
        contratada no mesmo ano.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Locações ──
    st.subheader("Locações de imóveis por dispensa")
    loc = carregar_tce("locacoes_imoveis.csv")

    if not loc.empty:
        loc["Valor total do contrato"] = pd.to_numeric(
            loc["Valor total do contrato"].str.replace(",", "."), errors="coerce"
        )

        top_loc = loc.nlargest(10, "Valor total do contrato")
        fig_loc = go.Figure(go.Bar(
            x=top_loc["Valor total do contrato"] / 1e3,
            y=top_loc["Nome da empresa contratada"],
            orientation="h",
            marker_color="#f4a261",
            hovertemplate="R$ %{x:,.1f} mil<extra></extra>",
        ))
        fig_loc.update_layout(
            xaxis=dict(tickprefix="R$ ", ticksuffix=" mil"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=380,
        )
        st.plotly_chart(fig_loc, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            pf = loc[loc["CNPJ da empresa contratada"].isna()]
            st.metric("Contratos com pessoas físicas",
                      f"{len(pf)} de {len(loc)}",
                      delta=f"R$ {pf['Valor total do contrato'].sum()/1e3:,.1f} mil")
        with col2:
            st.metric("Maior contrato único",
                      f"R$ {loc['Valor total do contrato'].max()/1e3:,.1f} mil",
                      delta="INDÚSTRIA ALUMÍNIO ABC")

        st.markdown("""
        <div class="alerta-medio">
        ⚠️ <strong>BRAULIO + SILVANA BUENO DE ALMEIDA</strong> — mesmo sobrenome composto,
        valores idênticos (R$ 225k cada), mesmo dia (19/04/2021). Total: R$ 450.000.<br>
        ⚠️ <strong>SILVIO + REGINA CHAGAS</strong> — mesmo sobrenome, valores idênticos
        (R$ 111k cada), mesmo dia (20/05/2022). Total: R$ 222.015.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Convênios ──
    st.subheader("Convênios federais — alertas")
    st.markdown("""
    <div class="alerta">
    🔴 <strong>INADIMPLENTE</strong> — V Festival Cultural Raízes (2007): R$ 250.000 recebidos
    do Ministério do Turismo. Prestação de contas nunca regularizada.<br>
    🟠 <strong>INADIMPLÊNCIA SUSPENSA</strong> — Equipamentos educação infantil (2006):
    R$ 90.090 recebidos do FNDE. Situação irregular há quase 20 anos.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ok">
    ✅ <strong>Medicamentos (2024)</strong> — 607 dispensas analisadas. Padrão compatível
    com reposição semestral de farmácia municipal. Sem irregularidades identificadas.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("Fonte: TCE-SP · Portal da Transparência Federal · Dados: 2021–2024")

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA 4 — LIMITES CONSTITUCIONAIS (AUDESP)
# ════════════════════════════════════════════════════════════════════════════

elif pagina == "📋 Limites Constitucionais":

    st.subheader("📋 Limites Constitucionais — AUDESP")
    st.caption("Fonte: TCE-SP · Resultado das Análises AUDESP · 2016–2025")

    audesp = carregar_audesp()

    if audesp.empty:
        st.warning("Dados AUDESP não encontrados em data/processed/tce_sp/audesp_ferraz.csv")
    else:
        audesp["Exercício"] = pd.to_numeric(audesp["Exercício"], errors="coerce")
        audesp = audesp.sort_values("Exercício")

        ano_audesp = audesp[audesp["Exercício"] == ano_selecionado]
        if not ano_audesp.empty:
            row = ano_audesp.iloc[0]
            col1, col2, col3 = st.columns(3)
            with col1:
                ensino = row.get("Despesa Empenhada Ensino (%)", None)
                val = f"{ensino*100:.1f}%" if pd.notna(ensino) else "s/d"
                delta = "✓ acima do mínimo" if pd.notna(ensino) and ensino >= 0.25 else "⚠ abaixo do mínimo"
                st.metric("Ensino (mín. 25%)", val, delta=delta,
                          delta_color="normal" if pd.notna(ensino) and ensino >= 0.25 else "inverse")
            with col2:
                saude = row.get("Despesa Empenhada Saúde (%)", None)
                val = f"{saude*100:.1f}%" if pd.notna(saude) else "s/d"
                delta = "✓ acima do mínimo" if pd.notna(saude) and saude >= 0.15 else "⚠ abaixo do mínimo"
                st.metric("Saúde (mín. 15%)", val, delta=delta,
                          delta_color="normal" if pd.notna(saude) and saude >= 0.15 else "inverse")
            with col3:
                pessoal = row.get("Despesa com Pessoal Poder Executivo (%)", None)
                val = f"{pessoal*100:.1f}%" if pd.notna(pessoal) else "s/d"
                delta = "✓ dentro do limite" if pd.notna(pessoal) and pessoal <= 0.54 else "⚠ acima do limite"
                st.metric("Pessoal (lim. 54%)", val, delta=delta,
                          delta_color="normal" if pd.notna(pessoal) and pessoal <= 0.54 else "inverse")

        st.divider()
        st.subheader("Evolução dos indicadores — 2016 a 2025")

        fig_aud = go.Figure()
        fig_aud.add_trace(go.Scatter(
            x=audesp["Exercício"],
            y=audesp["Despesa Empenhada Ensino (%)"] * 100,
            name="Ensino", line=dict(color="#2196F3", width=2),
            hovertemplate="%{y:.1f}%<extra>Ensino</extra>"
        ))
        fig_aud.add_trace(go.Scatter(
            x=audesp["Exercício"],
            y=audesp["Despesa Empenhada Saúde (%)"] * 100,
            name="Saúde", line=dict(color="#e63946", width=2),
            hovertemplate="%{y:.1f}%<extra>Saúde</extra>"
        ))
        fig_aud.add_trace(go.Scatter(
            x=audesp["Exercício"],
            y=audesp["Despesa com Pessoal Poder Executivo (%)"] * 100,
            name="Pessoal", line=dict(color="#f4a261", width=2),
            hovertemplate="%{y:.1f}%<extra>Pessoal</extra>"
        ))

        anos_range = [audesp["Exercício"].min(), audesp["Exercício"].max()]
        for y, name, color in [
            (25, "Mín. Ensino (25%)", "#2196F3"),
            (15, "Mín. Saúde (15%)", "#e63946"),
            (54, "Lim. Pessoal (54%)", "#f4a261"),
        ]:
            fig_aud.add_trace(go.Scatter(
                x=anos_range, y=[y, y], name=name,
                line=dict(color=color, width=1, dash="dash"), showlegend=True
            ))

        fig_aud.update_layout(
            xaxis=dict(tickmode="linear", dtick=1),
            yaxis=dict(ticksuffix="%"),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=10, b=0),
            height=420,
        )
        st.plotly_chart(fig_aud, use_container_width=True)

        st.markdown("""
        <div class="alerta">
        ⚠️ <strong>2016</strong> — Despesa com pessoal atingiu 54,9%, ultrapassando o limite
        da LRF (54%). Gestão anterior.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="ok">
        ✅ <strong>Gestão atual (2022–2024)</strong> — Ensino e Saúde dentro dos limites
        constitucionais em todos os anos analisados.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("Fonte: TCE-SP / AUDESP · Dados: 2016–2025")

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA 5 — CONTEXTO SOCIOECONÔMICO
# ════════════════════════════════════════════════════════════════════════════

elif pagina == "🏙️ Contexto Socioeconômico":

    st.subheader("🏙️ Contexto Socioeconômico — Ferraz de Vasconcelos")
    st.caption("Fonte: IBGE · Censo 2022 · PNUD · DATASUS · Dados de referência")

    ibge = carregar_ibge()

    if not ibge.empty:
        def get(indicador):
            row = ibge[ibge["indicador"] == indicador]
            if not row.empty:
                return row.iloc[0]["valor"], int(row.iloc[0]["ano"])
            return None, None

        st.subheader("População e território")
        col1, col2, col3 = st.columns(3)
        with col1:
            v, a = get("populacao_censo")
            st.metric("População (Censo)", f"{int(v):,}".replace(",", "."), delta=f"Censo {a}")
        with col2:
            v, a = get("populacao_estimada")
            st.metric("População estimada", f"{int(v):,}".replace(",", "."), delta=str(a))
        with col3:
            v, a = get("densidade_demografica")
            st.metric("Densidade demográfica", f"{v:,.0f} hab/km²", delta=str(a))

        st.divider()
        st.subheader("Economia e renda")
        col1, col2, col3 = st.columns(3)
        with col1:
            v, a = get("pib_per_capita")
            st.metric("PIB per capita", f"R$ {v:,.2f}", delta=str(a))
        with col2:
            v, a = get("idhm")
            st.metric("IDHM", f"{v:.3f}", delta=f"{a} — desatualizado")
        with col3:
            v, a = get("salario_medio_formal")
            st.metric("Salário médio formal", f"{v:.1f} SM", delta=str(a))

        col1, col2, col3 = st.columns(3)
        with col1:
            v, a = get("empregos_formais")
            st.metric("Empregos formais", f"{int(v):,}".replace(",", "."), delta=str(a))
        with col2:
            v, a = get("pop_ate_meio_sm")
            st.metric("Pop. até ½ SM", f"{v:.0f}%", delta=f"{a} — contexto pobreza")
        with col3:
            v, a = get("transferencias_correntes_pct")
            st.metric("Dependência de repasses", f"{v:.1f}%", delta=f"da receita em {a}")

        st.divider()
        st.subheader("Educação")
        col1, col2, col3 = st.columns(3)
        with col1:
            v, a = get("escolarizacao_6_14")
            st.metric("Escolarização 6–14 anos", f"{v:.2f}%", delta=str(a))
        with col2:
            v, a = get("ideb_fundamental_inicial")
            st.metric("IDEB Fund. Inicial", f"{v:.1f}", delta=str(a))
        with col3:
            v, a = get("ideb_fundamental_final")
            st.metric("IDEB Fund. Final", f"{v:.1f}", delta=str(a))

        st.divider()
        st.subheader("Saúde e infraestrutura")
        col1, col2, col3 = st.columns(3)
        with col1:
            v, a = get("mortalidade_infantil")
            st.metric("Mortalidade infantil", f"{v:.1f}/mil nascidos", delta=str(a))
        with col2:
            v, a = get("esgotamento_sanitario")
            st.metric("Esgotamento sanitário", f"{v:.2f}%", delta=str(a))
        with col3:
            v, a = get("urbanizacao_vias")
            st.metric("Urbanização de vias", f"{v:.1f}%",
                      delta=f"{a} — déficit explica obras CASAMAX",
                      delta_color="off")

        st.markdown("""
        <div class="alerta">
        ⚠️ <strong>Contexto importante para a análise:</strong><br>
        Com apenas <strong>11,8% de urbanização de vias</strong> (2010) e <strong>37% da população
        com renda até ½ salário mínimo</strong>, Ferraz tem déficits reais de infraestrutura.
        Isso contextualiza — mas não justifica — o volume de contratos com a CASAMAX (R$ 87,5mi)
        e a DATACITY (R$ 46,9mi). A questão central permanece: <em>os valores pagos foram justos
        e os serviços foram entregues?</em>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("Mortalidade — DATASUS 2020–2024")

    obitos_ano = pd.DataFrame([
        {"Ano": 2020, "Óbitos": 1223},
        {"Ano": 2021, "Óbitos": 1532},
        {"Ano": 2022, "Óbitos": 1173},
        {"Ano": 2023, "Óbitos": 1129},
        {"Ano": 2024, "Óbitos": 1197},
    ])

    obitos_causa = pd.DataFrame([
        {"Causa": "Doenças circulatórias",  "Óbitos": 1414},
        {"Causa": "Neoplasias",             "Óbitos": 856},
        {"Causa": "Causas mal definidas",   "Óbitos": 854},
        {"Causa": "Doenças infecciosas",    "Óbitos": 792},
        {"Causa": "Doenças respiratórias",  "Óbitos": 625},
        {"Causa": "Causas externas",        "Óbitos": 419},
        {"Causa": "Doenças endócrinas",     "Óbitos": 361},
        {"Causa": "Doenças digestivas",     "Óbitos": 269},
        {"Causa": "Doenças geniturinárias", "Óbitos": 219},
        {"Causa": "Doenças neurológicas",   "Óbitos": 168},
    ])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de óbitos 2020–2024", "6.254")
        st.metric("Causas mal definidas", "13,7%",
                  delta="⚠ acima do esperado (<5%)", delta_color="inverse")

        fig_ano = go.Figure(go.Bar(
            x=obitos_ano["Ano"], y=obitos_ano["Óbitos"],
            marker_color=["#e63946" if a == 2021 else "#2196F3" for a in obitos_ano["Ano"]],
            hovertemplate="%{y} óbitos<extra></extra>",
        ))
        fig_ano.update_layout(
            title="Óbitos por ano",
            xaxis=dict(tickmode="linear", dtick=1),
            margin=dict(l=0, r=0, t=30, b=0), height=250,
        )
        st.plotly_chart(fig_ano, use_container_width=True)

    with col2:
        fig_causa = go.Figure(go.Bar(
            x=obitos_causa["Óbitos"], y=obitos_causa["Causa"],
            orientation="h",
            marker_color=["#e63946" if c == "Causas mal definidas"
                          else "#f4a261" if c == "Causas externas"
                          else "#2196F3" for c in obitos_causa["Causa"]],
            hovertemplate="%{x} óbitos<extra></extra>",
        ))
        fig_causa.update_layout(
            title="Óbitos por causa (2020–2024)",
            margin=dict(l=0, r=0, t=30, b=0), height=350,
        )
        st.plotly_chart(fig_causa, use_container_width=True)

    st.markdown("""
    <div class="alerta">
    ⚠️ <strong>Causas mal definidas: 13,7%</strong> dos óbitos sem diagnóstico claro —
    acima do esperado para municípios bem estruturados (&lt;5%).<br>
    🔴 <strong>Pico 2021</strong> — aumento de 25% em relação a 2020, reflexo da COVID-19.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("Fonte: IBGE Cidades · Censo 2022 · PNUD 2010 · DATASUS 2023")