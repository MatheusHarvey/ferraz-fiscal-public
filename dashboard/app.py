import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
        .ok { background: #f0fff4; border-left: 4px solid #2d6a4f;
              padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0; }
    </style>
""", unsafe_allow_html=True)

SICONFI_DIR = Path("data/processed/siconfi")
TCE_DIR     = Path("data/processed/tce_sp")
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
    ["📊 Visão Geral", "⚠️ Alertas e Irregularidades", "📋 Indicadores AUDESP", "🏙️ Contexto Socioeconômico"]
)
st.sidebar.divider()
st.sidebar.title("Filtros")
ano_selecionado = st.sidebar.selectbox("Ano", ANOS, index=len(ANOS)-1)

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 — VISÃO GERAL
# ════════════════════════════════════════════════════════════════════════════

if pagina == "📊 Visão Geral":

    receitas       = carregar_siconfi("receitas")
    despesas       = carregar_siconfi("despesas")
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

    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Receita Total", formatar_reais(receita_total))
    with col2:
        st.metric("Despesa Total", formatar_reais(despesa_total))
    with col3:
        st.metric("Saldo", formatar_reais(saldo), delta=formatar_reais(saldo))

    st.divider()

    # Evolução anual
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

    # Despesas por função
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
# PÁGINA 2 — ALERTAS E IRREGULARIDADES
# ════════════════════════════════════════════════════════════════════════════

elif pagina == "⚠️ Alertas e Irregularidades":

    st.subheader("⚠️ Alertas e Irregularidades — TCE-SP")
    st.caption("Fonte: Portal da Transparência Municipal do TCE-SP · Dados: 2021–2024")

    # Resumo geral
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Casos de fracionamento", "10", delta="2022–2024", delta_color="inverse")
    with col2:
        st.metric("Locações suspeitas", "19", delta="R$ 2,77 mi", delta_color="inverse")
    with col3:
        st.metric("Total investigado", "R$ 3,67 mi", delta="em dispensas", delta_color="inverse")

    st.divider()

    # ── Fracionamento ──
    st.subheader("Fracionamento de despesa")
    frac = carregar_tce("suspeitos_fracionamento.csv")

    if not frac.empty:
        frac["valor_total"] = pd.to_numeric(frac["valor_total"], errors="coerce")
        frac["qtd_contratos"] = pd.to_numeric(frac["qtd_contratos"], errors="coerce")

        # Gráfico
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
        🔴 <strong>E DE SOUZA LOPES</strong> — empresa com situação BAIXADA na Receita Federal. 
        A baixa ocorreu em ago/2025, após os contratos de 2024.<br>
        ⚠️ <strong>W & MACEDO ELÉTRICA</strong> — CNAE de comércio varejista, contratada para obras de engenharia.<br>
        ⚠️ <strong>JA RODRIGUES ARQUITETURA</strong> — empresa aberta em jul/2024 e já contratada no mesmo ano.
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

        # Gráfico top locações
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
        <div class="alerta">
        ⚠️ <strong>BRAULIO + SILVANA BUENO DE ALMEIDA</strong> — mesmo sobrenome composto, 
        valores idênticos (R$ 225k cada), mesmo dia. Total: R$ 450.000.<br>
        ⚠️ <strong>SILVIO + REGINA CHAGAS</strong> — mesmo sobrenome, valores idênticos 
        (R$ 111k cada), mesmo dia. Total: R$ 222.015.
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
    ✅ <strong>Medicamentos (2024)</strong> — 607 dispensas analisadas. 
    Volume alto concentrado em 2 processos em março e 1 em dezembro. 
    Padrão compatível com reposição semestral de farmácia municipal. Sem irregularidades.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 — INDICADORES AUDESP
# ════════════════════════════════════════════════════════════════════════════

elif pagina == "📋 Indicadores AUDESP":

    st.subheader("📋 Indicadores AUDESP — Limites Constitucionais")
    st.caption("Fonte: TCE-SP · Resultado das Análises AUDESP · 2016–2025")

    audesp = carregar_audesp()

    if audesp.empty:
        st.warning("Dados AUDESP não encontrados em data/processed/tce_sp/audesp_ferraz.csv")
    else:
        audesp["Exercício"] = pd.to_numeric(audesp["Exercício"], errors="coerce")
        audesp = audesp.sort_values("Exercício")

        # Métricas do ano selecionado
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

        # Gráfico evolução dos 3 indicadores
        st.subheader("Evolução dos indicadores — 2016 a 2025")

        fig_aud = go.Figure()

        # Ensino
        fig_aud.add_trace(go.Scatter(
            x=audesp["Exercício"],
            y=audesp["Despesa Empenhada Ensino (%)"] * 100,
            name="Ensino", line=dict(color="#2196F3", width=2),
            hovertemplate="%{y:.1f}%<extra>Ensino</extra>"
        ))

        # Saúde
        fig_aud.add_trace(go.Scatter(
            x=audesp["Exercício"],
            y=audesp["Despesa Empenhada Saúde (%)"] * 100,
            name="Saúde", line=dict(color="#e63946", width=2),
            hovertemplate="%{y:.1f}%<extra>Saúde</extra>"
        ))

        # Pessoal
        fig_aud.add_trace(go.Scatter(
            x=audesp["Exercício"],
            y=audesp["Despesa com Pessoal Poder Executivo (%)"] * 100,
            name="Pessoal", line=dict(color="#f4a261", width=2),
            hovertemplate="%{y:.1f}%<extra>Pessoal</extra>"
        ))

        # Linhas de limite
        anos_range = [audesp["Exercício"].min(), audesp["Exercício"].max()]
        fig_aud.add_trace(go.Scatter(
            x=anos_range, y=[25, 25], name="Mín. Ensino (25%)",
            line=dict(color="#2196F3", width=1, dash="dash"), showlegend=True
        ))
        fig_aud.add_trace(go.Scatter(
            x=anos_range, y=[15, 15], name="Mín. Saúde (15%)",
            line=dict(color="#e63946", width=1, dash="dash"), showlegend=True
        ))
        fig_aud.add_trace(go.Scatter(
            x=anos_range, y=[54, 54], name="Lim. Pessoal (54%)",
            line=dict(color="#f4a261", width=1, dash="dash"), showlegend=True
        ))

        fig_aud.update_layout(
            xaxis=dict(tickmode="linear", dtick=1),
            yaxis=dict(ticksuffix="%"),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=10, b=0),
            height=420,
        )
        st.plotly_chart(fig_aud, use_container_width=True)

        # Alerta histórico
        st.markdown("""
        <div class="alerta">
        ⚠️ <strong>2016</strong> — Despesa com pessoal atingiu 54,9%, ultrapassando o limite da LRF (54%). 
        Gestão anterior.<br>
        ⚠️ <strong>Saúde 2021–2023</strong> — Índice próximo ao mínimo de 15%. 
        Monitoramento contínuo recomendado.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="ok">
        ✅ <strong>Gestão atual (2022–2024)</strong> — Ensino e Saúde dentro dos limites constitucionais 
        em todos os anos analisados.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("Fonte: TCE-SP / AUDESP · Dados: 2016–2025")
elif pagina == "🏙️ Contexto Socioeconômico":

    st.subheader("🏙️ Contexto Socioeconômico — Ferraz de Vasconcelos")
    st.caption("Fonte: IBGE · Censo 2022 · PNUD · Dados de referência para análise dos gastos públicos")

    ibge = carregar_ibge()

    if ibge.empty:
        st.warning("Dados IBGE não encontrados em data/processed/ibge/ibge_ferraz.csv")
    else:
        def get(indicador):
            row = ibge[ibge["indicador"] == indicador]
            if not row.empty:
                return row.iloc[0]["valor"], int(row.iloc[0]["ano"])
            return None, None

        st.divider()
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

        st.divider()
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
        st.caption("Fonte: IBGE Cidades · Censo Demográfico 2022 · PNUD 2010 · DATASUS 2023")