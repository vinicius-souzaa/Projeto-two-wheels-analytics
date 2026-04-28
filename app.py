"""
LM 2 Rodas - Dashboard de Inteligencia de Mercado & Planejamento Comercial
Marcas: X11 | Scud | Vessel | HighOne | Sentec | WG Sports
Distribuidora B2B | Grupo LAGOApar
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import (
    carregar_vendas, carregar_vendedores, carregar_estoque,
    carregar_metas, carregar_metas_canal, carregar_projecoes, carregar_catalogo,
    fR, delta_pct,
)

# ── Configuracao ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LM 2 Rodas · Inteligencia de Mercado",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paleta de cores LM 2 Rodas ────────────────────────────────────────────────
C = {
    "azul_escuro":  "#00285F",
    "azul_medio":   "#0055A5",
    "azul_claro":   "#2F80CC",
    "azul_bg":      "#EBF4FF",
    "laranja":      "#FF6B00",
    "laranja_claro":"#FF8C42",
    "branco":       "#FFFFFF",
    "cinza_claro":  "#F4F7FB",
    "cinza_texto":  "#4A5568",
    "verde":        "#1B7A34",
    "verde_claro":  "#D5F5E3",
    "vermelho":     "#C0392B",
    "vermelho_claro":"#FADBD8",
    "amarelo":      "#B7770D",
    "amarelo_claro":"#FEF9E7",
}

# Cores por marca — 6 cores bem distintas entre si
MARCA_CORES = {
    "X11":       "#FF6B00",  # laranja vibrante  (identidade X11)
    "Scud":      "#0055A5",  # azul corporativo  (identidade LM)
    "Vessel":    "#7D3C98",  # roxo              (diferenciado)
    "HighOne":   "#1B7A34",  # verde escuro      (natureza/bike)
    "Sentec":    "#00897B",  # verde-azulado/teal (tech/componentes)
    "WG Sports": "#C0392B",  # vermelho          (energia/esporte)
}

PAGINAS = {
    "resumo":    "Resumo Executivo",
    "comercial": "Força de Vendas B2B",
    "produto":   "Análise por Produto",
    "regional":  "Análise Regional",
    "estoque":   "Estoque e Giro",
    "metas":     "Metas e FP&A",
    "projecoes": "Projeções",
}
ICONES = {
    "resumo":    "⚡",
    "comercial": "📈",
    "produto":   "🏷️",
    "regional":  "🗺️",
    "estoque":   "📦",
    "metas":     "🎯",
    "projecoes": "🔮",
}

# ── CSS global ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Fonte global +20% (Streamlit base ~14px -> ~17px) */
  html, body {{ font-size: 17px !important; }}
  .stApp, .stMarkdown p, .stMarkdown li, .stText {{ font-size: 1rem !important; }}
  label, .stSelectbox label, .stMultiSelect label {{ font-size: 0.95rem !important; }}

  /* Sidebar */
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, {C['azul_escuro']} 0%, {C['azul_medio']} 100%);
  }}
  [data-testid="stSidebar"] * {{ color: {C['branco']} !important; }}

  /* Botoes de navegacao (paginas inativas) — estilizados como links */
  [data-testid="stSidebar"] .stButton > button {{
      background: transparent !important;
      border: none !important;
      border-radius: 8px !important;
      color: rgba(255,255,255,0.82) !important;
      font-size: 0.95rem !important;
      font-weight: 500 !important;
      text-align: left !important;
      justify-content: flex-start !important;
      padding: 11px 15px !important;
      width: 100% !important;
      transition: background 0.18s ease !important;
      box-shadow: none !important;
  }}
  [data-testid="stSidebar"] .stButton > button:hover {{
      background: rgba(255,255,255,0.15) !important;
      color: {C['branco']} !important;
      border: none !important;
      box-shadow: none !important;
  }}
  [data-testid="stSidebar"] .stButton > button:focus:not(:active) {{
      box-shadow: none !important;
      border: none !important;
      outline: none !important;
  }}
  /* Pagina ativa — renderizada como div HTML, nao como botao */
  .nav-ativo {{
      display: block;
      background: {C['laranja']};
      border-radius: 8px;
      padding: 11px 15px;
      margin: 3px 0;
      font-size: 0.95rem;
      font-weight: 700;
      color: {C['branco']} !important;
  }}

  /* KPI cards */
  .kpi-card {{
      background: {C['branco']};
      border-radius: 12px;
      padding: 18px 22px;
      border-top: 4px solid {C['azul_medio']};
      box-shadow: 0 2px 10px rgba(0,85,165,0.10);
      margin-bottom: 6px;
  }}
  .kpi-card.dest {{ border-top-color: {C['laranja']}; }}
  .kpi-card h4 {{
      color: {C['cinza_texto']};
      font-size: 0.78rem;
      margin: 0;
      letter-spacing: 0.07em;
      text-transform: uppercase;
  }}
  .kpi-card p {{
      color: {C['azul_escuro']};
      font-size: 2rem;
      font-weight: 800;
      margin: 6px 0 2px;
      line-height: 1;
  }}
  .kpi-card small {{ font-size: 0.85rem; }}

  /* Secao */
  .sec-hdr {{
      border-left: 4px solid {C['azul_medio']};
      padding-left: 13px;
      margin: 24px 0 4px;
  }}
  .sec-hdr h3 {{ color: {C['azul_escuro']}; font-size: 1.1rem; margin: 0; }}
  .sec-hdr .desc {{ color: {C['cinza_texto']}; font-size: 0.88rem; margin: 3px 0 0; font-style: italic; }}

  /* Disclaimer */
  .disclaimer {{
      background: #FFF8E1;
      border-left: 4px solid #F59E0B;
      border-radius: 6px;
      padding: 8px 14px;
      font-size: 0.83rem !important;
      color: #78350F;
      margin: 4px 0 16px;
  }}

  /* RAG cards */
  .rag-grid {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 8px 0 16px; }}
  .rag-card {{
      flex: 1; min-width: 220px;
      border-radius: 10px;
      padding: 14px 18px;
      display: flex; align-items: flex-start; gap: 12px;
  }}
  .rag-card .dot {{
      width: 18px; height: 18px; border-radius: 50%;
      flex-shrink: 0; margin-top: 2px;
      box-shadow: 0 0 6px rgba(0,0,0,0.25);
  }}
  .rag-card .body .badge {{
      font-size: 0.70rem; font-weight: 700;
      letter-spacing: 0.08em; text-transform: uppercase;
      margin: 0 0 3px;
  }}
  .rag-card .body .msg {{ font-size: 0.90rem; margin: 0; }}
  .rag-verde   {{ background:{C['verde_claro']};   border:1px solid {C['verde']}; }}
  .rag-amarelo {{ background:{C['amarelo_claro']}; border:1px solid {C['amarelo']}; }}
  .rag-vermelho{{ background:{C['vermelho_claro']};border:1px solid {C['vermelho']}; }}
  .dot-verde   {{ background:{C['verde']}; }}
  .dot-amarelo {{ background:{C['amarelo']}; }}
  .dot-vermelho{{ background:{C['vermelho']}; }}
  .badge-verde  {{ color:{C['verde']}; }}
  .badge-amarelo{{ color:{C['amarelo']}; }}
  .badge-vermelho{{ color:{C['vermelho']}; }}
</style>
""", unsafe_allow_html=True)


# ── Roteamento por query param ────────────────────────────────────────────────
pagina_atual = st.query_params.get("page", "resumo")
if pagina_atual not in PAGINAS:
    pagina_atual = "resumo"


# ── Helpers ───────────────────────────────────────────────────────────────────
def kpi(titulo, valor, delta=None, destaque=False):
    classe = "kpi-card dest" if destaque else "kpi-card"
    delta_html = ""
    if delta is not None:
        cor   = C["verde"] if delta >= 0 else C["vermelho"]
        sinal = "▲" if delta >= 0 else "▼"
        delta_html = f'<small style="color:{cor}">{sinal} {abs(delta):.1f}% vs mes anterior</small>'
    st.markdown(
        f'<div class="{classe}"><h4>{titulo}</h4><p>{valor}</p>{delta_html}</div>',
        unsafe_allow_html=True,
    )


def hdr(titulo, desc=""):
    desc_html = f'<p class="desc">{desc}</p>' if desc else ""
    st.markdown(
        f'<div class="sec-hdr"><h3>{titulo}</h3>{desc_html}</div>',
        unsafe_allow_html=True,
    )


def aviso_dados():
    st.markdown(
        '<div class="disclaimer">⚠️ <strong>Dados sintéticos</strong> — '
        'simulados com base em benchmarks reais do mercado brasileiro de duas rodas. '
        'Exclusivamente para fins de demonstração analítica.</div>',
        unsafe_allow_html=True,
    )


def rag(status, badge, mensagem):
    """status: 'verde' | 'amarelo' | 'vermelho'"""
    rotulos = {"verde": "SAUDÁVEL", "amarelo": "ATENÇÃO", "vermelho": "CRÍTICO"}
    label = badge or rotulos.get(status, status.upper())
    return (
        f'<div class="rag-card rag-{status}">'
        f'<div class="dot dot-{status}"></div>'
        f'<div class="body">'
        f'<p class="badge badge-{status}">{label}</p>'
        f'<p class="msg">{mensagem}</p>'
        f'</div></div>'
    )


def plt_layout(fig, h=390):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter,sans-serif", color=C["cinza_texto"], size=14),
        height=h,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, bgcolor="rgba(0,0,0,0)",
            font_size=13,
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor="#D0D8E4", tickfont_size=13)
    fig.update_yaxes(gridcolor="#EBF0F8", linecolor="#D0D8E4", tickfont_size=13)
    return fig


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="text-align:center;padding:18px 0 10px;">'
        f'<span style="font-size:2.4rem;">🏍️</span><br>'
        f'<span style="font-size:1.2rem;font-weight:900;letter-spacing:.05em;">LM 2 RODAS</span><br>'
        f'<span style="font-size:0.72rem;opacity:.72;letter-spacing:.10em;text-transform:uppercase;">'
        f'Inteligência de Mercado</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    # Navegacao: pagina ativa = div HTML (laranja); inativas = st.button transparente.
    # st.button faz apenas st.rerun() — mesma sessao WebSocket, filtros preservados.
    for key, nome in PAGINAS.items():
        if key == pagina_atual:
            # Ativo: renderizado como HTML (nao pode ser clicado, ja esta na pagina)
            st.markdown(
                f'<div class="nav-ativo">{ICONES[key]} {nome}</div>',
                unsafe_allow_html=True,
            )
        else:
            # Inativo: botao estilizado via CSS geral do sidebar
            if st.button(f"{ICONES[key]} {nome}", key=f"nav_{key}", width="stretch"):
                st.query_params["page"] = key
                st.rerun()

    st.divider()

    df_v_raw   = carregar_vendas()
    marcas_disp = sorted(df_v_raw["marca"].unique())
    marcas_sel  = st.multiselect("Marca", marcas_disp, default=marcas_disp, key="f_marca")

    # Periodo agora e date_input com granularidade diaria.
    data_min = df_v_raw["data_dt"].min().date()
    data_max = df_v_raw["data_dt"].max().date()
    periodo = st.date_input(
        "Período",
        value=(data_min, data_max),
        min_value=data_min, max_value=data_max,
        format="DD/MM/YYYY",
        key="f_per",
    )
    # Trata o caso em que o usuario ainda nao selecionou as duas datas
    if isinstance(periodo, tuple) and len(periodo) == 2:
        data_ini, data_fim = periodo
    else:
        data_ini, data_fim = data_min, data_max

    canais_disp = sorted(df_v_raw["canal"].unique())
    canais_sel  = st.multiselect("Canal", canais_disp, default=canais_disp, key="f_canal")

    seg_disp  = sorted(df_v_raw["segmento"].unique())
    seg_sel   = st.multiselect("Segmento", seg_disp, default=seg_disp, key="f_seg")

    st.divider()
    st.caption(f"LAGOApar · Nova Lima, MG\n{data_min:%d/%m/%Y} – {data_max:%d/%m/%Y}")

# Strings ISO usadas para filtrar (vendas: dia-a-dia; tabelas mensais: por mes)
data_ini_s = data_ini.strftime("%Y-%m-%d")
data_fim_s = data_fim.strftime("%Y-%m-%d")
mes_ini    = data_ini.strftime("%Y-%m")
mes_fim    = data_fim.strftime("%Y-%m")


# ── Filtros globais ───────────────────────────────────────────────────────────
# Vendas filtradas por DIA (granularidade diaria); demais tabelas por MES
dfF = df_v_raw[
    df_v_raw["marca"].isin(marcas_sel) &
    (df_v_raw["data"] >= data_ini_s) &
    (df_v_raw["data"] <= data_fim_s) &
    df_v_raw["canal"].isin(canais_sel) &
    df_v_raw["segmento"].isin(seg_sel)
].copy()

meses_p   = sorted(dfF["mes"].unique())
m_atual   = meses_p[-1] if meses_p else mes_fim
m_ant     = meses_p[-2] if len(meses_p) > 1 else m_atual

rec_total = dfF["receita"].sum()
qtd_total = dfF["quantidade"].sum()
mg_total  = dfF["margem_bruta"].sum()
mg_pct    = mg_total / rec_total * 100 if rec_total else 0
rec_atual = dfF[dfF["mes"] == m_atual]["receita"].sum()
rec_ant   = dfF[dfF["mes"] == m_ant]["receita"].sum()
ticket_md = rec_total / qtd_total if qtd_total else 0

# Bug #3: YoY agora respeita o filtro de periodo. Compara o periodo selecionado
# com o MESMO subperiodo do ano anterior (ex: jan-jun/2025 vs jan-jun/2024).
# Granularidade diaria — usa coluna 'data' em vez de 'mes'.
def _yoy_periodo(df_raw, d_ini, d_fim, marcas_, canais_, segs_):
    """Receita atual e receita do mesmo subperiodo do ano anterior (em dias)."""
    rec_atual_p = df_raw[
        df_raw["marca"].isin(marcas_) &
        (df_raw["data"] >= d_ini) & (df_raw["data"] <= d_fim) &
        df_raw["canal"].isin(canais_) &
        df_raw["segmento"].isin(segs_)
    ]["receita"].sum()
    # mesmo periodo do ano anterior
    ini_ant = (pd.to_datetime(d_ini) - pd.DateOffset(years=1)).strftime("%Y-%m-%d")
    fim_ant = (pd.to_datetime(d_fim) - pd.DateOffset(years=1)).strftime("%Y-%m-%d")
    rec_ant_p = df_raw[
        df_raw["marca"].isin(marcas_) &
        (df_raw["data"] >= ini_ant) & (df_raw["data"] <= fim_ant) &
        df_raw["canal"].isin(canais_) &
        df_raw["segmento"].isin(segs_)
    ]["receita"].sum()
    return rec_atual_p, rec_ant_p, ini_ant, fim_ant

rec_atual_yoy, rec_anterior_yoy, yoy_ini_ant, yoy_fim_ant = _yoy_periodo(
    df_v_raw, data_ini_s, data_fim_s, marcas_sel, canais_sel, seg_sel
)
yoy = delta_pct(rec_atual_yoy, rec_anterior_yoy) if rec_anterior_yoy > 0 else 0.0
yoy_disponivel = rec_anterior_yoy > 0


# ═══════════════════════════════════════════════════════════════════════════════
# P1 — RESUMO EXECUTIVO
# ═══════════════════════════════════════════════════════════════════════════════
if pagina_atual == "resumo":
    st.title("⚡ Resumo Executivo")
    aviso_dados()
    st.caption(
        f"Período: {pd.to_datetime(data_ini_s):%d/%m/%Y} → "
        f"{pd.to_datetime(data_fim_s):%d/%m/%Y}  |  "
        f"Marcas selecionadas: {', '.join(marcas_sel)}"
    )

    # KPIs principais
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: kpi("Receita Total",        fR(rec_total), destaque=True)
    with c2: kpi("Receita Último Mês",   fR(rec_atual), delta=delta_pct(rec_atual, rec_ant))
    with c3: kpi("Margem Bruta Média",   f"{mg_pct:.1f}%")
    with c4: kpi("Unidades Vendidas",    f"{qtd_total:,}")
    with c5: kpi("Ticket Médio",         fR(ticket_md))
    with c6:
        if yoy_disponivel:
            kpi("Crescimento YoY", f"{yoy:+.1f}%", destaque=(yoy > 0))
        else:
            kpi("Crescimento YoY", "n/d")

    st.divider()

    # Alertas RAG
    hdr("Painel de Alertas — Semáforo RAG",
        "Indicadores sintéticos de saúde do negócio com base nos dados do período selecionado")

    d_rec = delta_pct(rec_atual, rec_ant)
    if d_rec >= 5:
        card_receita = rag("verde", None, f"Crescimento de {d_rec:.1f}% no último mês — acima do gatilho de +5%")
    elif d_rec >= 0:
        card_receita = rag("amarelo", None, f"Crescimento de {d_rec:.1f}% — dentro do intervalo esperado (0–5%)")
    else:
        card_receita = rag("vermelho", None, f"Queda de {abs(d_rec):.1f}% na receita mensal — requer plano de ação")

    if mg_pct >= 42:
        card_margem = rag("verde", None, f"Margem bruta {mg_pct:.1f}% — acima do alvo de 42%")
    elif mg_pct >= 36:
        card_margem = rag("amarelo", None, f"Margem bruta {mg_pct:.1f}% — entre 36–42%, zona de atenção")
    else:
        card_margem = rag("vermelho", None, f"Margem bruta {mg_pct:.1f}% — abaixo do mínimo de 36%")

    if not yoy_disponivel:
        card_yoy = rag("amarelo", "CRESCIMENTO YoY",
                       "Período anterior (mesmo intervalo do ano passado) sem dados — YoY indisponível.")
    elif yoy >= 10:
        card_yoy = rag("verde", "CRESCIMENTO YoY",
                       f"Receita do período supera o mesmo intervalo do ano anterior em {yoy:.1f}% — ritmo forte")
    elif yoy >= 0:
        card_yoy = rag("amarelo", "CRESCIMENTO YoY",
                       f"Crescimento YoY de {yoy:.1f}% — monitorar aceleração")
    else:
        card_yoy = rag("vermelho", "CRESCIMENTO YoY",
                       f"Receita recuou {abs(yoy):.1f}% vs mesmo período do ano anterior — investigar causas")

    df_canal_r = dfF.groupby("canal")["receita"].sum()
    top_canal  = df_canal_r.idxmax() if not df_canal_r.empty else "—"
    share_top  = df_canal_r.max() / rec_total * 100 if rec_total else 0
    if share_top <= 50:
        card_canal = rag("verde", "MIX DE CANAL", f"Canal líder '{top_canal}' com {share_top:.0f}% — diversificação saudável")
    elif share_top <= 65:
        card_canal = rag("amarelo", "MIX DE CANAL", f"'{top_canal}' representa {share_top:.0f}% — dependência moderada")
    else:
        card_canal = rag("vermelho", "MIX DE CANAL", f"'{top_canal}' concentra {share_top:.0f}% da receita — risco de concentração")

    df_marca_r  = dfF.groupby("marca")["receita"].sum()
    top_marca   = df_marca_r.idxmax() if not df_marca_r.empty else "—"
    share_marca = df_marca_r.max() / rec_total * 100 if rec_total else 0
    if share_marca <= 50:
        card_marca = rag("verde", "MIX DE MARCA", f"'{top_marca}' lidera com {share_marca:.0f}% — portfólio equilibrado")
    elif share_marca <= 65:
        card_marca = rag("amarelo", "MIX DE MARCA", f"'{top_marca}' com {share_marca:.0f}% — dependência de marca acima do ideal")
    else:
        card_marca = rag("vermelho", "MIX DE MARCA", f"'{top_marca}' concentra {share_marca:.0f}% — risco de dependência")

    df_cid_r    = dfF.groupby("cidade")["receita"].sum()
    top_cid     = df_cid_r.idxmax() if not df_cid_r.empty else "—"
    share_cid   = df_cid_r.max() / rec_total * 100 if rec_total else 0
    if share_cid <= 20:
        card_geo = rag("verde", "CONCENTRAÇÃO GEO", f"Sem concentração excessiva: '{top_cid}' com {share_cid:.0f}%")
    elif share_cid <= 35:
        card_geo = rag("amarelo", "CONCENTRAÇÃO GEO", f"'{top_cid}' responde por {share_cid:.0f}% — diversificar presença")
    else:
        card_geo = rag("vermelho", "CONCENTRAÇÃO GEO", f"'{top_cid}' com {share_cid:.0f}% — alta concentração geográfica")

    # Renderiza o grid de RAG
    st.markdown(
        f'<div class="rag-grid">{card_receita}{card_margem}{card_yoy}'
        f'{card_canal}{card_marca}{card_geo}</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    col_a, col_b = st.columns([2, 1])

    with col_a:
        hdr("Receita Mensal por Marca",
            "Evolução da receita para cada marca do portfólio no período selecionado — "
            "identifique tendências de crescimento, sazonalidade e comparativos entre marcas.")
        df_t = dfF.groupby(["mes", "marca"])["receita"].sum().reset_index()
        fig  = px.line(df_t, x="mes", y="receita", color="marca",
                       color_discrete_map=MARCA_CORES,
                       labels={"mes": "", "receita": "Receita (R$)", "marca": "Marca"})
        fig.update_traces(line_width=2.5)
        st.plotly_chart(plt_layout(fig), width="stretch")

    with col_b:
        hdr("Participação de Receita por Marca",
            "Share percentual de cada marca no total do período — "
            "quanto cada marca contribui para o faturamento consolidado.")
        df_mix = dfF.groupby("marca")["receita"].sum().reset_index()
        fig = px.pie(df_mix, values="receita", names="marca",
                     color="marca", color_discrete_map=MARCA_CORES, hole=0.50)
        fig.update_traces(textfont_size=13)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=390,
            margin=dict(l=8, r=8, t=40, b=8),
            legend=dict(orientation="h", y=-0.14, font_size=12),
        )
        st.plotly_chart(fig, width="stretch")

    col_c, col_d = st.columns(2)

    with col_c:
        hdr("Top 12 Produtos — Receita Acumulada",
            "Ranking dos produtos com maior faturamento no período. "
            "Use para priorizar mix de estoque, negociações e campanhas comerciais.")
        df_top = (
            dfF.groupby("produto")["receita"].sum()
            .nlargest(12).reset_index().sort_values("receita")
        )
        fig = px.bar(df_top, x="receita", y="produto", orientation="h",
                     color_discrete_sequence=[C["azul_medio"]], text_auto=".2s")
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=420,
            margin=dict(l=8, r=8, t=30, b=8),
            yaxis_title="", xaxis_title="Receita (R$)",
        )
        fig.update_yaxes(tickfont_size=11)
        st.plotly_chart(fig, width="stretch")

    with col_d:
        hdr("Receita por Canal e Segmento",
            "Distribuição da receita entre os canais de venda (Varejo, E-commerce, "
            "Distribuidores, Marketplace) separada por segmento Moto vs Bike.")
        df_cs = dfF.groupby(["canal", "segmento"])["receita"].sum().reset_index()
        fig = px.bar(df_cs, x="canal", y="receita", color="segmento",
                     barmode="group",
                     color_discrete_map={"Moto": C["azul_medio"], "Bike": C["laranja"]},
                     text_auto=".2s")
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=420,
            margin=dict(l=8, r=8, t=40, b=8),
            yaxis_title="Receita (R$)", xaxis_title="",
            legend=dict(orientation="h", y=1.06, font_size=13),
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#EBF0F8")
        st.plotly_chart(fig, width="stretch")

    # Crescimento YoY por marca — Bug #3: respeita o filtro de periodo
    st.divider()
    _ini_label = pd.to_datetime(data_ini_s).strftime("%d/%m/%Y")
    _fim_label = pd.to_datetime(data_fim_s).strftime("%d/%m/%Y")
    _ini_ant_label = pd.to_datetime(yoy_ini_ant).strftime("%d/%m/%Y")
    _fim_ant_label = pd.to_datetime(yoy_fim_ant).strftime("%d/%m/%Y")
    hdr(f"Crescimento por Marca — {_ini_label} a {_fim_label} vs {_ini_ant_label} a {_fim_ant_label}",
        "Comparativo de receita entre o período selecionado e o mesmo subperíodo do ano anterior, "
        "por marca. Mostra quais marcas ganharam ou perderam tração no intervalo escolhido.")
    if yoy_disponivel:
        # atual (filtrado)
        df_atual_marca = dfF.groupby("marca")["receita"].sum()
        # ano anterior — filtra por data (granularidade diaria)
        df_ant = df_v_raw[
            df_v_raw["marca"].isin(marcas_sel) &
            (df_v_raw["data"] >= yoy_ini_ant) & (df_v_raw["data"] <= yoy_fim_ant) &
            df_v_raw["canal"].isin(canais_sel) &
            df_v_raw["segmento"].isin(seg_sel)
        ]
        df_ant_marca = df_ant.groupby("marca")["receita"].sum()
        df_pivot = pd.DataFrame({
            "atual":    df_atual_marca,
            "anterior": df_ant_marca,
        }).fillna(0).reset_index()
        df_pivot["crescimento_pct"] = (
            (df_pivot["atual"] - df_pivot["anterior"]) /
            df_pivot["anterior"].replace(0, np.nan) * 100
        ).round(1)
        df_pivot = df_pivot.dropna(subset=["crescimento_pct"]).sort_values("crescimento_pct")
        if not df_pivot.empty:
            cores_yoy = [C["verde"] if v >= 0 else C["vermelho"] for v in df_pivot["crescimento_pct"]]
            fig = go.Figure(go.Bar(
                x=df_pivot["crescimento_pct"], y=df_pivot["marca"],
                orientation="h", marker_color=cores_yoy,
                text=[f"{v:+.1f}%" for v in df_pivot["crescimento_pct"]],
                textposition="outside", textfont_size=13,
            ))
            fig.add_vline(x=0, line_color=C["azul_escuro"], line_width=1.5)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=300,
                margin=dict(l=8, r=8, t=30, b=8),
                xaxis_title="Variação % vs mesmo período do ano anterior", yaxis_title="",
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Sem marcas com dados em ambos os períodos para o comparativo.")
    else:
        st.info(
            f"O período selecionado ({_ini_label} a {_fim_label}) não tem ano anterior "
            "disponível no dataset. Ajuste o filtro para incluir um intervalo com ao menos "
            "um ano de histórico anterior."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# P2 — FORCA DE VENDAS B2B
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina_atual == "comercial":
    st.title("📈 Força de Vendas B2B")
    aviso_dados()
    st.info(
        "**Contexto:** A LM 2 Rodas opera como distribuidora B2B — vende para mais de 20.000 "
        "lojistas e distribuidores em todo o Brasil. Esta página acompanha o desempenho dos "
        "representantes comerciais regionais e dos canais de distribuição.",
        icon="ℹ️",
    )

    df_ve = carregar_vendedores()
    dfV   = df_ve[(df_ve["mes"] >= mes_ini) & (df_ve["mes"] <= mes_fim)].copy()

    t_real   = dfV["receita_realizada"].sum()
    t_meta   = dfV["meta_receita"].sum()
    ating    = t_real / t_meta * 100 if t_meta else 0
    cli_tot  = dfV["clientes_atendidos"].sum()
    # Bug #6: ticket medio agregado correto (receita / clientes), nao media de medias
    tick_med = t_real / cli_tot if cli_tot else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Receita Realizada",    fR(t_real), destaque=True)
    with c2: kpi("Meta Acumulada",       fR(t_meta))
    with c3: kpi("Atingimento Geral",    f"{ating:.1f}%")
    with c4: kpi("Clientes Atendidos",   f"{cli_tot:,}")
    with c5: kpi("Ticket Médio",         fR(tick_med))

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Atingimento de Meta por Representante (%)",
            "Percentual da meta de receita atingida por cada representante comercial. "
            "Verde = 100% ou acima. Amarelo = 90–100%. Vermelho = abaixo de 90%.")
        df_va = dfV.groupby("vendedor").agg(
            realizado=("receita_realizada", "sum"),
            meta=("meta_receita", "sum"),
        ).reset_index()
        df_va["ating"] = (df_va["realizado"] / df_va["meta"] * 100).round(1)
        df_va = df_va.sort_values("ating")
        cores = [
            C["verde"] if v >= 100 else C["amarelo"] if v >= 90 else C["vermelho"]
            for v in df_va["ating"]
        ]
        fig = go.Figure(go.Bar(
            x=df_va["ating"], y=df_va["vendedor"],
            orientation="h", marker_color=cores,
            text=[f"{v:.1f}%" for v in df_va["ating"]],
            textposition="outside", textfont_size=13,
        ))
        fig.add_vline(x=100, line_dash="dash", line_color=C["laranja"], line_width=2,
                      annotation_text="Meta 100%", annotation_font_size=13)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=400,
            margin=dict(l=8, r=8, t=36, b=8),
            xaxis_title="% da Meta", yaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=12)
        st.plotly_chart(fig, width="stretch")

    with col_b:
        hdr("Evolução Mensal de Receita por Representante",
            "Acompanhamento mês a mês da receita de cada representante. "
            "Permite identificar sazonalidade, quedas pontuais e tendências individuais.")
        df_tv = dfV.groupby(["mes", "vendedor"])["receita_realizada"].sum().reset_index()
        fig   = px.line(df_tv, x="mes", y="receita_realizada", color="vendedor",
                        labels={"mes": "", "receita_realizada": "Receita (R$)", "vendedor": ""})
        fig.update_traces(line_width=2)
        st.plotly_chart(plt_layout(fig, h=400), width="stretch")

    hdr("Receita vs Meta por Canal de Distribuição",
        "Comparativo entre receita realizada e meta estabelecida para cada canal B2B — "
        "Varejo Físico, E-commerce, Distribuidores e Marketplace. "
        "Metas são pré-definidas por canal (não recalculadas a cada filtro).")
    # Bug #1: usa metas_canal.csv (deterministicas) ao inves de np.random.uniform
    df_mc = carregar_metas_canal()
    df_mcF = df_mc[(df_mc["mes"] >= mes_ini) & (df_mc["mes"] <= mes_fim)]
    df_canal_v = df_mcF.groupby("canal").agg(
        receita=("receita_realizada", "sum"),
        meta_canal=("meta_receita", "sum"),
    ).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Meta", x=df_canal_v["canal"], y=df_canal_v["meta_canal"],
                         marker_color=C["azul_claro"], opacity=0.7))
    fig.add_trace(go.Bar(name="Realizado", x=df_canal_v["canal"], y=df_canal_v["receita"],
                         marker_color=C["azul_escuro"]))
    fig.update_layout(
        barmode="group", paper_bgcolor="rgba(0,0,0,0)", height=340,
        margin=dict(l=8, r=8, t=36, b=8),
        legend=dict(orientation="h", y=1.06, font_size=13),
        yaxis_title="Receita (R$)", xaxis_title="",
    )
    fig.update_xaxes(showgrid=False, tickfont_size=13)
    fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
    st.plotly_chart(fig, width="stretch")

    st.divider()
    hdr("Ranking de Representantes no Período",
        "Visão consolidada do desempenho de cada representante — região de atuação, "
        "receita, meta e percentual de atingimento.")
    # Bug #10: aproveita a regiao_atuacao adicionada no gerar_vendedores
    df_va_full = dfV.groupby(["vendedor", "regiao_atuacao"]).agg(
        realizado=("receita_realizada", "sum"),
        meta=("meta_receita", "sum"),
        clientes=("clientes_atendidos", "sum"),
    ).reset_index()
    df_va_full["ating"] = (df_va_full["realizado"] / df_va_full["meta"] * 100).round(1)
    df_det = df_va_full.sort_values("ating", ascending=False).copy()
    df_det["realizado_fmt"] = df_det["realizado"].map(fR)
    df_det["meta_fmt"]      = df_det["meta"].map(fR)
    df_det["ating_fmt"]     = df_det["ating"].map(lambda x: f"{x:.1f}%")
    st.dataframe(
        df_det[["vendedor", "regiao_atuacao", "realizado_fmt", "meta_fmt",
                "clientes", "ating_fmt"]]
        .rename(columns={
            "vendedor": "Representante",
            "regiao_atuacao": "Região",
            "realizado_fmt": "Receita Realizada",
            "meta_fmt": "Meta",
            "clientes": "Clientes Atendidos",
            "ating_fmt": "Atingimento (%)",
        }),
        width="stretch", hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# P3 — ANALISE POR PRODUTO
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina_atual == "produto":
    st.title("🏷️ Análise por Produto")
    aviso_dados()

    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Receita por Categoria de Produto",
            "Faturamento acumulado de cada categoria no período selecionado. "
            "Identifica quais linhas de produto são mais relevantes para a receita.")
        df_cat = (dfF.groupby("categoria")["receita"].sum()
                  .reset_index().sort_values("receita", ascending=False))
        fig = px.bar(df_cat, x="categoria", y="receita",
                     color="categoria",
                     color_discrete_sequence=[
                         C["azul_escuro"], C["azul_medio"], C["azul_claro"],
                         C["laranja"], "#7D3C98", "#00897B", C["vermelho"], "#E67E22"
                     ],
                     text_auto=".2s")
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=380,
            margin=dict(l=8, r=8, t=30, b=8),
            showlegend=False, yaxis_title="Receita (R$)", xaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=12)
        fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
        st.plotly_chart(fig, width="stretch")

    with col_b:
        hdr("Margem Bruta por Categoria (%)",
            "Percentual de margem bruta de cada categoria. Permite identificar quais linhas "
            "são mais rentáveis e onde há pressão de custo ou desconto excessivo.")
        df_mg = dfF.groupby("categoria").agg(
            receita=("receita", "sum"),
            margem=("margem_bruta", "sum"),
        ).reset_index()
        df_mg = df_mg[df_mg["receita"] > 0].copy()
        df_mg["mg_pct"] = (df_mg["margem"] / df_mg["receita"] * 100).round(1)
        df_mg = df_mg.sort_values("mg_pct")
        fig = px.bar(df_mg, x="mg_pct", y="categoria", orientation="h",
                     color="mg_pct",
                     color_continuous_scale=[
                         [0, C["vermelho"]], [0.45, C["amarelo"]], [1, C["verde"]]
                     ],
                     range_color=[25, 55], text_auto=".1f")
        fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside", textfont_size=12)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=380,
            margin=dict(l=8, r=8, t=30, b=8),
            coloraxis_showscale=False,
            xaxis_title="Margem Bruta (%)", yaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(tickfont_size=12)
        st.plotly_chart(fig, width="stretch")

    hdr("Heatmap de Receita: Marca × Categoria",
        "Mapa de calor que cruza cada marca com suas categorias de produto. "
        "Células mais escuras = maior receita. Identifica gaps de portfólio e concentração.")
    # Bug #8: protege contra df vazio
    if dfF.empty:
        st.info("Sem dados no filtro selecionado para o heatmap.")
    else:
        df_heat = dfF.pivot_table(
            index="marca", columns="categoria", values="receita",
            aggfunc="sum", fill_value=0,
        )
        if df_heat.empty or df_heat.values.sum() == 0:
            st.info("Sem dados no filtro selecionado para o heatmap.")
        else:
            fig = px.imshow(
                df_heat,
                color_continuous_scale=[[0, C["cinza_claro"]], [0.4, C["azul_claro"]], [1, C["azul_escuro"]]],
                text_auto=".2s", aspect="auto",
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=290,
                margin=dict(l=8, r=8, t=36, b=8),
                font_size=13,
            )
            st.plotly_chart(fig, width="stretch")

    # ABC Curve
    st.divider()
    hdr("Curva ABC de Produtos — Classificação por Receita",
        "Classifica os SKUs em três grupos: A (top 80% da receita), B (próximos 15%) e C (5% restante). "
        "Produtos A exigem prioridade em estoque, margem e reposição; C podem ser revisados.")
    df_abc = dfF.groupby(["sku", "produto", "marca", "categoria"]).agg(
        receita=("receita", "sum"),
        margem=("margem_bruta", "sum"),
        qtd=("quantidade", "sum"),
    ).reset_index()
    df_abc = df_abc[df_abc["receita"] > 0].sort_values("receita", ascending=False)
    df_abc["receita_acum"] = df_abc["receita"].cumsum()
    total_abc = df_abc["receita"].sum()
    df_abc["pct_acum"] = df_abc["receita_acum"] / total_abc * 100
    df_abc["classe"] = df_abc["pct_acum"].apply(
        lambda x: "A" if x <= 80 else ("B" if x <= 95 else "C")
    )
    df_abc["mg_pct"] = (df_abc["margem"] / df_abc["receita"] * 100).round(1)

    c_abc1, c_abc2, c_abc3 = st.columns(3)
    for cls, col, cor in [("A", c_abc1, C["verde"]), ("B", c_abc2, C["amarelo"]), ("C", c_abc3, C["vermelho"])]:
        n = (df_abc["classe"] == cls).sum()
        r = df_abc[df_abc["classe"] == cls]["receita"].sum()
        with col:
            st.markdown(
                f'<div style="background:{cor}18;border:1px solid {cor};border-radius:10px;'
                f'padding:14px 18px;text-align:center;">'
                f'<p style="font-size:1.6rem;font-weight:800;color:{cor};margin:0;">{n} SKUs</p>'
                f'<p style="font-size:0.9rem;color:{C["cinza_texto"]};margin:4px 0 0;">'
                f'Classe {cls} — {fR(r)} ({r/total_abc*100:.0f}% da receita) </p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    col_abc_a, col_abc_b = st.columns(2)
    with col_abc_a:
        fig_abc = px.bar(
            df_abc.head(25), x="receita", y="produto", orientation="h",
            color="classe",
            color_discrete_map={"A": C["verde"], "B": C["amarelo"], "C": C["vermelho"]},
            text_auto=".2s",
        )
        fig_abc.update_traces(textposition="outside", textfont_size=11)
        fig_abc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=540,
            margin=dict(l=8, r=8, t=36, b=8),
            yaxis_title="", xaxis_title="Receita (R$)",
            legend=dict(orientation="h", y=1.04, font_size=13),
        )
        fig_abc.update_yaxes(tickfont_size=10)
        fig_abc.update_xaxes(showgrid=False, tickfont_size=13)
        st.plotly_chart(fig_abc, width="stretch")

    with col_abc_b:
        # Scatter receita x margem pct colorido por classe ABC
        fig_sc = px.scatter(
            df_abc, x="receita", y="mg_pct",
            color="classe",
            color_discrete_map={"A": C["verde"], "B": C["amarelo"], "C": C["vermelho"]},
            size="qtd", hover_name="produto", size_max=35,
            labels={"receita": "Receita (R$)", "mg_pct": "Margem (%)", "classe": "Classe ABC"},
        )
        fig_sc.add_hline(y=df_abc["mg_pct"].mean(), line_dash="dash",
                         line_color=C["azul_escuro"],
                         annotation_text=f"Média {df_abc['mg_pct'].mean():.1f}%",
                         annotation_font_size=12)
        st.plotly_chart(plt_layout(fig_sc, h=540), width="stretch")

    hdr("Catálogo Completo de Produtos")
    df_cat_full = carregar_catalogo()
    st.dataframe(
        df_cat_full[["sku", "nome", "marca", "categoria", "segmento", "preco", "custo", "margem_pct"]]
        .rename(columns={
            "sku": "SKU", "nome": "Produto", "marca": "Marca",
            "categoria": "Categoria", "segmento": "Segmento",
            "preco": "Preço (R$)", "custo": "Custo (R$)", "margem_pct": "Margem (%)",
        }),
        width="stretch", hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# P4 — ANALISE REGIONAL
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina_atual == "regional":
    st.title("🗺️ Análise Regional")
    aviso_dados()

    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Receita por Região do Brasil",
            "Faturamento acumulado por macro-região. Reflete a cobertura nacional "
            "da LM 2 Rodas com representantes em todos os estados.")
        df_reg = dfF.groupby("regiao")["receita"].sum().reset_index().sort_values("receita", ascending=False)
        fig = px.bar(df_reg, x="regiao", y="receita",
                     color="receita",
                     color_continuous_scale=[[0, C["azul_claro"]], [1, C["azul_escuro"]]],
                     text_auto=".2s")
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=380,
            margin=dict(l=8, r=8, t=30, b=8),
            coloraxis_showscale=False,
            yaxis_title="Receita (R$)", xaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
        st.plotly_chart(fig, width="stretch")

    with col_b:
        hdr("Top 15 Cidades — Receita",
            "Ranking das cidades com maior faturamento. Cor indica a macro-região. "
            "Orienta a alocação de representantes e esforço comercial por praça.")
        df_cid = dfF.groupby(["cidade", "uf", "regiao"])["receita"].sum().reset_index()
        df_cid = df_cid.nlargest(15, "receita").sort_values("receita")
        df_cid["cidade_uf"] = df_cid["cidade"] + " (" + df_cid["uf"] + ")"
        fig = px.bar(df_cid, x="receita", y="cidade_uf", orientation="h",
                     color="regiao",
                     color_discrete_sequence=[
                         C["azul_escuro"], C["azul_medio"], C["laranja"],
                         C["verde"], C["azul_claro"]
                     ],
                     text_auto=".2s")
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=460,
            margin=dict(l=8, r=8, t=30, b=8),
            yaxis_title="", xaxis_title="Receita (R$)",
            legend=dict(orientation="h", y=1.05, font_size=12),
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(tickfont_size=11)
        st.plotly_chart(fig, width="stretch")

    hdr("Heatmap: Receita por Região × Marca",
        "Mapa de calor cruzando região com marca. Identifica quais marcas dominam "
        "cada território e onde há oportunidades de expansão para marcas sub-representadas.")
    # Bug #8: protege contra df vazio
    if dfF.empty:
        st.info("Sem dados no filtro selecionado para o heatmap.")
    else:
        df_rm = dfF.pivot_table(
            index="regiao", columns="marca", values="receita",
            aggfunc="sum", fill_value=0,
        )
        if df_rm.empty or df_rm.values.sum() == 0:
            st.info("Sem dados no filtro selecionado para o heatmap.")
        else:
            fig = px.imshow(
                df_rm,
                color_continuous_scale=[[0, C["cinza_claro"]], [0.4, C["azul_claro"]], [1, C["azul_escuro"]]],
                text_auto=".2s", aspect="auto",
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=290,
                margin=dict(l=8, r=8, t=36, b=8), font_size=13,
            )
            st.plotly_chart(fig, width="stretch")

    col_c, col_d = st.columns(2)

    with col_c:
        hdr("Evolução de Receita por Região — Mensal",
            "Tendência mensal de cada macro-região. Permite identificar regiões "
            "em crescimento, sazonalidade local e regiões que precisam de atenção.")
        df_revol = dfF.groupby(["mes", "regiao"])["receita"].sum().reset_index()
        fig = px.line(df_revol, x="mes", y="receita", color="regiao",
                      labels={"mes": "", "receita": "Receita (R$)", "regiao": "Regiao"})
        fig.update_traces(line_width=2.2)
        st.plotly_chart(plt_layout(fig, h=370), width="stretch")

    with col_d:
        hdr("Receita por UF — Participação %",
            "Share de cada estado no faturamento total. Mostra em quais UFs "
            "a empresa tem maior penetração e onde há espaço para crescer.")
        df_uf = dfF.groupby("uf")["receita"].sum().reset_index().sort_values("receita", ascending=False).head(15)
        df_uf["share"] = (df_uf["receita"] / df_uf["receita"].sum() * 100).round(1)
        fig = px.bar(df_uf, x="uf", y="share",
                     color_discrete_sequence=[C["azul_medio"]], text_auto=".1f")
        fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside", textfont_size=12)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=370,
            margin=dict(l=8, r=8, t=30, b=8),
            yaxis_title="Share (%)", xaxis_title="Estado (UF)",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
        st.plotly_chart(fig, width="stretch")


# ═══════════════════════════════════════════════════════════════════════════════
# P5 — ESTOQUE & GIRO
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina_atual == "estoque":
    st.title("📦 Estoque & Giro")
    aviso_dados()

    df_est = carregar_estoque()
    # Bug #7: filtro respeita o periodo selecionado (era sempre o ultimo mes do dataset)
    df_est_periodo = df_est[
        df_est["marca"].isin(marcas_sel) &
        (df_est["mes"] >= mes_ini) & (df_est["mes"] <= mes_fim)
    ]
    if df_est_periodo.empty:
        st.info("Sem dados de estoque para o filtro selecionado.")
        st.stop()
    ult_mes_estoque = df_est_periodo["mes"].max()
    df_est_ult = df_est_periodo[df_est_periodo["mes"] == ult_mes_estoque].copy()

    t_est_val = df_est_ult["estoque_valor"].sum()
    # Bug #2: KPIs de giro/cobertura ignoram SKUs sem giro (vendido_mes=0),
    # caso contrario as medias ficam viesadas por produtos descontinuados
    df_est_ativo = df_est_ult[df_est_ult["vendido_mes"] > 0]
    giro_med  = df_est_ativo["giro_estoque"].mean() if not df_est_ativo.empty else 0
    cob_med   = df_est_ativo["cobertura_dias"].mean() if not df_est_ativo.empty else 0
    # Ruptura REAL = SKUs com vendas E cobertura baixa (nao = SKUs descontinuados)
    n_crit    = ((df_est_ult["vendido_mes"] > 0) &
                 (df_est_ult["cobertura_dias"] < 15)).sum()
    n_sem_giro = (df_est_ult["vendido_mes"] == 0).sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Valor em Estoque (Custo)", fR(t_est_val), destaque=True)
    with c2: kpi("Giro Médio de Estoque",    f"{giro_med:.2f}")
    with c3: kpi("Cobertura Média",          f"{cob_med:.0f} dias")
    with c4: kpi("Ruptura Iminente",         str(int(n_crit)))
    with c5: kpi("SKUs sem Giro",            str(int(n_sem_giro)))
    st.caption(f"Mês de referência do estoque: {ult_mes_estoque}")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Valor em Estoque por Categoria (R$ custo)",
            "Valor total do estoque ao custo de aquisição por categoria. "
            "Indica onde o capital está imobilizado e permite priorizar liquidez.")
        df_ec = (df_est_ult.groupby("categoria")["estoque_valor"].sum()
                 .reset_index().sort_values("estoque_valor", ascending=False))
        fig = px.bar(df_ec, x="categoria", y="estoque_valor",
                     color_discrete_sequence=[C["azul_medio"]], text_auto=".2s")
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=370,
            margin=dict(l=8, r=8, t=30, b=8),
            yaxis_title="Valor (R$)", xaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
        st.plotly_chart(fig, width="stretch")

    with col_b:
        hdr("Índice de Giro de Estoque por Marca",
            "Quantas vezes o estoque de cada marca 'girou' no mês mais recente. "
            "Giro alto = produto vendendo bem; giro baixo = risco de encalhamento.")
        df_eg = (df_est_ult.groupby("marca")["giro_estoque"].mean()
                 .reset_index().sort_values("giro_estoque"))
        cores_giro = [C["verde"] if v >= 0.8 else C["amarelo"] if v >= 0.4 else C["vermelho"]
                      for v in df_eg["giro_estoque"]]
        fig = go.Figure(go.Bar(
            x=df_eg["giro_estoque"], y=df_eg["marca"],
            orientation="h", marker_color=cores_giro,
            text=[f"{v:.2f}" for v in df_eg["giro_estoque"]],
            textposition="outside", textfont_size=13,
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=370,
            margin=dict(l=8, r=8, t=30, b=8),
            xaxis_title="Giro (un. vendidas / estoque)", yaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(tickfont_size=13)
        st.plotly_chart(fig, width="stretch")

    hdr("Evolução do Valor em Estoque — Mensal",
        "Histórico do valor imobilizado em estoque (ao custo) por marca. "
        "Picos podem indicar compras sazonais ou acúmulo de produtos sem giro.")
    df_est_filt = df_est[
        df_est["marca"].isin(marcas_sel) &
        (df_est["mes"] >= mes_ini) & (df_est["mes"] <= mes_fim)
    ]
    df_est_tr = df_est_filt.groupby(["mes", "marca"])["estoque_valor"].sum().reset_index()
    fig = px.line(df_est_tr, x="mes", y="estoque_valor", color="marca",
                  color_discrete_map=MARCA_CORES,
                  labels={"mes": "", "estoque_valor": "Valor em Estoque (R$)", "marca": "Marca"})
    fig.update_traces(line_width=2.2)
    st.plotly_chart(plt_layout(fig, h=330), width="stretch")

    st.divider()
    # Bug #2: separa "ruptura iminente" (com demanda + cobertura baixa) de
    # "SKU sem giro" (sem demanda — provavel descontinuacao)
    col_alert1, col_alert2 = st.columns(2)

    with col_alert1:
        hdr("🔴 Ruptura Iminente (com demanda)",
            "SKUs que ESTÃO vendendo mas com estoque insuficiente para cobrir 15 dias. "
            "Ação: reposição urgente.")
        df_rup = df_est_ult[
            (df_est_ult["vendido_mes"] > 0) &
            (df_est_ult["cobertura_dias"] < 15)
        ].sort_values("cobertura_dias")
        if df_rup.empty:
            st.success("✅ Nenhum SKU em ruptura iminente.")
        else:
            st.warning(f"⚠️ {len(df_rup)} SKUs — reposição imediata.")
            st.dataframe(
                df_rup[["sku", "produto", "marca", "estoque_unidades",
                        "vendido_mes", "cobertura_dias"]]
                .rename(columns={
                    "sku": "SKU", "produto": "Produto", "marca": "Marca",
                    "estoque_unidades": "Estoque (un)", "vendido_mes": "Vendido/mês",
                    "cobertura_dias": "Cobertura (dias)",
                }),
                width="stretch", hide_index=True,
            )

    with col_alert2:
        hdr("🟡 SKUs sem Giro (revisar portfólio)",
            "SKUs sem vendas no mês de referência. Candidatos a descontinuação, "
            "promoção ou revisão de mix. Não é ruptura de estoque.")
        df_sem = df_est_ult[df_est_ult["vendido_mes"] == 0].copy()
        if df_sem.empty:
            st.success("✅ Todos os SKUs venderam no mês.")
        else:
            st.info(f"ℹ️ {len(df_sem)} SKUs sem giro — avaliar descontinuação.")
            st.dataframe(
                df_sem[["sku", "produto", "marca", "estoque_unidades",
                        "estoque_valor"]]
                .rename(columns={
                    "sku": "SKU", "produto": "Produto", "marca": "Marca",
                    "estoque_unidades": "Estoque (un)",
                    "estoque_valor": "Capital Imobilizado (R$)",
                }),
                width="stretch", hide_index=True,
            )


# ═══════════════════════════════════════════════════════════════════════════════
# P6 — METAS & FP&A
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina_atual == "metas":
    st.title("🎯 Metas & FP&A")
    aviso_dados()

    df_mt  = carregar_metas()
    df_mtF = df_mt[
        df_mt["marca"].isin(marcas_sel) &
        (df_mt["mes"] >= mes_ini) & (df_mt["mes"] <= mes_fim)
    ].copy()

    t_real = df_mtF["receita_realizada"].sum()
    t_meta = df_mtF["meta_receita"].sum()
    var    = delta_pct(t_real, t_meta)
    mg_acc = df_mtF["margem_bruta"].sum()
    mg_pct_m = mg_acc / t_real * 100 if t_real else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Receita Realizada",  fR(t_real), destaque=True)
    with c2: kpi("Meta Acumulada",     fR(t_meta))
    with c3: kpi("Variação vs Meta",   f"{var:+.1f}%")
    with c4: kpi("Margem Bruta Média", f"{mg_pct_m:.1f}%")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Realizado vs Meta por Marca",
            "Comparativo entre receita realizada e meta estabelecida para cada marca. "
            "Barras sobrepostas revelam quais marcas superaram ou ficaram abaixo do planejado (acumulado no período).")
        df_bm = df_mtF.groupby("marca").agg(
            realizado=("receita_realizada", "sum"),
            meta=("meta_receita", "sum"),
        ).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Meta", x=df_bm["marca"], y=df_bm["meta"],
                             marker_color=C["azul_claro"], opacity=0.7))
        fig.add_trace(go.Bar(name="Realizado", x=df_bm["marca"], y=df_bm["realizado"],
                             marker_color=C["azul_escuro"]))
        fig.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", height=370,
            margin=dict(l=8, r=8, t=36, b=8),
            legend=dict(orientation="h", y=1.05, font_size=13),
            yaxis_title="R$", xaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
        st.plotly_chart(fig, width="stretch")

    with col_b:
        hdr("Evolução Mensal — Realizado vs Meta",
            "Série histórica da receita realizada (área preenchida) versus a meta mensal "
            "(linha tracejada). A área entre as linhas representa o gap a ser gerenciado.")
        df_tM = df_mtF.groupby("mes").agg(
            realizado=("receita_realizada", "sum"),
            meta=("meta_receita", "sum"),
        ).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_tM["mes"], y=df_tM["meta"],
            name="Meta", line=dict(dash="dash", color=C["laranja"], width=2),
            mode="lines",
        ))
        fig.add_trace(go.Scatter(
            x=df_tM["mes"], y=df_tM["realizado"],
            name="Realizado", line=dict(color=C["azul_escuro"], width=2.5),
            fill="tonexty", fillcolor="rgba(0,85,165,0.10)", mode="lines",
        ))
        st.plotly_chart(plt_layout(fig, h=370), width="stretch")

    col_c, col_d = st.columns(2)

    with col_c:
        hdr("Variação % vs Meta — Linha do Tempo",
            "Desvio percentual mensal entre receita realizada e meta. "
            "Barras verdes = superou a meta; barras vermelhas = ficou abaixo.")
        df_var = df_mtF.groupby("mes").agg(
            realizado=("receita_realizada", "sum"),
            meta=("meta_receita", "sum"),
        ).reset_index()
        df_var["var_pct"] = (
            (df_var["realizado"] - df_var["meta"]) / df_var["meta"] * 100
        ).round(1)
        fig = px.bar(df_var, x="mes", y="var_pct",
                     color=df_var["var_pct"].apply(lambda x: "Acima" if x >= 0 else "Abaixo"),
                     color_discrete_map={"Acima": C["verde"], "Abaixo": C["vermelho"]},
                     text_auto=".1f")
        fig.add_hline(y=0, line_color=C["azul_escuro"], line_width=1.5)
        fig.update_traces(texttemplate="%{y:+.1f}%", textposition="outside", textfont_size=11)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=340,
            margin=dict(l=8, r=8, t=30, b=8),
            showlegend=False, yaxis_title="Var. % vs Meta", xaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=12)
        fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
        st.plotly_chart(fig, width="stretch")

    with col_d:
        hdr("Margem Bruta por Marca — Acumulado",
            "Percentual de margem bruta por marca no período — cada barra reflete a estrutura de custo "
            "específica da marca. WG Sports e Vessel lideram margem; Sentec e HighOne têm estrutura de custo maior.")
        df_mg_m = df_mtF.groupby("marca").agg(
            margem=("margem_bruta", "sum"),
            receita=("receita_realizada", "sum"),
        ).reset_index()
        df_mg_m = df_mg_m[df_mg_m["receita"] > 0].copy()
        df_mg_m["mg_pct"] = (df_mg_m["margem"] / df_mg_m["receita"] * 100).round(1)
        df_mg_m = df_mg_m.sort_values("mg_pct")
        fig = px.bar(df_mg_m, x="mg_pct", y="marca", orientation="h",
                     color="marca", color_discrete_map=MARCA_CORES,
                     text_auto=".1f")
        fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside", textfont_size=12)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=340,
            margin=dict(l=8, r=8, t=30, b=8),
            showlegend=False, xaxis_title="Margem Bruta (%)", yaxis_title="",
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(tickfont_size=13)
        st.plotly_chart(fig, width="stretch")


# ═══════════════════════════════════════════════════════════════════════════════
# P7 — PROJECOES
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina_atual == "projecoes":
    st.title("🔮 Projeções — Mai–Out 2026")
    aviso_dados()

    df_pr = carregar_projecoes()

    c1, c2, c3 = st.columns(3)
    with c1: kpi("Receita Projetada (6 meses)", fR(df_pr["receita_projetada"].sum()), destaque=True)
    with c2: kpi("Cenário Otimista",             fR(df_pr["receita_otimista"].sum()))
    with c3: kpi("Cenário Pessimista",           fR(df_pr["receita_pessimista"].sum()))

    # ── Caixa de explicação do modelo ────────────────────────────────────────
    with st.expander("📐 Metodologia e Confiabilidade do Modelo", expanded=True):
        # Métricas fixas validadas na avaliação comparativa (eval_models.py)
        MAPE_SARIMA  = 8.24    # MAPE out-of-sample 6 meses (nov/2025–abr/2026)
        R2_SARIMA    = 0.9359
        # CoV da série histórica completa
        df_hist_all = df_v_raw.groupby("mes")["receita"].sum().reset_index().sort_values("mes")
        rec_series  = df_hist_all["receita"].values
        cov = (rec_series.std() / rec_series.mean() * 100) if rec_series.mean() > 0 else 0
        # Spread dos cenários gerados pelo IC 90% do SARIMA
        ot_spread = (df_pr["receita_otimista"].mean() / df_pr["receita_projetada"].mean() - 1) * 100
        pe_spread = (1 - df_pr["receita_pessimista"].mean() / df_pr["receita_projetada"].mean()) * 100

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Modelo", "SARIMA(1,1,1)(1,1,1,12)",
                      help="Selecionado por avaliação comparativa com 14 modelos: Naive, ARIMA, SARIMA, Holt-Winters, Linear, Ridge, Lasso, Random Forest, Gradient Boosting, XGBoost, Prophet")
        with col_m2:
            st.metric("MAPE out-of-sample", f"{MAPE_SARIMA:.2f}%",
                      help="Erro médio absoluto percentual nos últimos 6 meses históricos (teste). Referência: modelo anterior tinha MAPE de 26.21%")
        with col_m3:
            st.metric("R² out-of-sample", f"{R2_SARIMA:.4f}",
                      help="Coeficiente de determinação — quanto da variância da série o modelo explica. Valores próximos de 1 indicam excelente ajuste")
        with col_m4:
            cor_cov = "🟢" if cov < 20 else "🟡" if cov < 35 else "🔴"
            st.metric(f"{cor_cov} CoV da Série Histórica", f"{cov:.1f}%",
                      help="Coeficiente de Variação — dispersão relativa da série. Valores < 20% indicam série estável")

        st.markdown(f"""
**Seleção do modelo — avaliação comparativa (14 modelos testados):**

| # | Modelo | MAPE | R² |
|---|---|---|---|
| 🥇 | **SARIMA(1,1,1)(1,1,1,12)** | **8.24%** | **0.936** |
| 🥈 | SARIMA(0,1,1)(0,1,1,12) | 8.51% | 0.937 |
| 🥉 | Gradient Boosting | 15.22% | 0.481 |
| — | Regressão Linear | 18.16% | 0.815 |
| — | Random Forest | 18.49% | 0.110 |
| — | XGBoost | 20.67% | 0.511 |
| — | ~~Modelo Anterior~~ | ~~26.21%~~ | ~~0.638~~ |
| — | Prophet | 28.65% | -0.058 |

**Como o modelo funciona:**
- **Parte regular (1,1,1):** captura tendência de curto prazo com diferenciação de 1ª ordem + componentes AR e MA
- **Parte sazonal (1,1,1,12):** captura o padrão anual de sazonalidade (período = 12 meses)
- **Cenário Base:** previsão pontual do SARIMA
- **Cenário Otimista / Pessimista:** limite superior e inferior do intervalo de confiança de **90%** — calculados estatisticamente pelo modelo, não por suposição manual
- **Melhora vs modelo anterior:** MAPE de 26,21% → 8,24% = **redução de 69% no erro**

**Limitações:**
- Série histórica de apenas 28 meses — o SARIMA sazonal fica mais robusto com 3+ ciclos anuais completos
- Não captura choques exógenos (câmbio, juros, ruptura de fornecedor)
- Margem projetada é estimada sobre o histórico consolidado — sem decomposição por marca
""")

    hdr("Cenários de Receita — Histórico + Projetado",
        "Gráfico combinando os últimos meses realizados com os três cenários de projeção "
        "(base, otimista, pessimista) para mai–out/2026. A área hachurada delimita o período projetado. "
        "Cenários calibrados com sazonalidade histórica e taxas de crescimento diferenciadas.")
    df_hist6 = dfF.groupby("mes")["receita"].sum().reset_index().tail(6)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_hist6["mes"], y=df_hist6["receita"],
        name="Historico", line=dict(color=C["azul_escuro"], width=2.5),
        mode="lines+markers", marker_size=8,
    ))
    fig.add_trace(go.Scatter(
        x=df_pr["mes"], y=df_pr["receita_pessimista"],
        name="Pessimista", line=dict(color=C["vermelho"], dash="dot", width=2),
        mode="lines",
    ))
    fig.add_trace(go.Scatter(
        x=df_pr["mes"], y=df_pr["receita_projetada"],
        name="Base", line=dict(color=C["azul_medio"], width=3),
        mode="lines+markers", marker_size=9,
    ))
    fig.add_trace(go.Scatter(
        x=df_pr["mes"], y=df_pr["receita_otimista"],
        name="Otimista", line=dict(color=C["verde"], dash="dot", width=2),
        fill="tonexty", fillcolor="rgba(27,122,52,0.07)", mode="lines",
    ))
    fig.add_vrect(
        x0=df_pr["mes"].iloc[0], x1=df_pr["mes"].iloc[-1],
        fillcolor=C["azul_claro"], opacity=0.05,
        annotation_text="Periodo Projetado",
        annotation_font_size=13,
        annotation_position="top left",
    )
    st.plotly_chart(plt_layout(fig, h=460), width="stretch")

    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Margem Bruta Projetada por Mês (%)",
            "Estimativa de margem bruta para cada mês do semestre projetado. "
            "A linha tracejada marca o alvo corporativo de 40%. Valores abaixo exigem revisão de pricing.")
        fig = px.bar(df_pr, x="mes", y="margem_projetada_pct",
                     color_discrete_sequence=[C["azul_medio"]], text_auto=".1f")
        fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside", textfont_size=12)
        fig.add_hline(y=40, line_dash="dash", line_color=C["laranja"], line_width=2,
                      annotation_text="Meta 40%", annotation_font_size=13)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=320,
            margin=dict(l=8, r=8, t=30, b=8),
            yaxis_title="Margem (%)", xaxis_title="",
            yaxis_range=[28, 55],
        )
        fig.update_xaxes(showgrid=False, tickfont_size=13)
        fig.update_yaxes(gridcolor="#EBF0F8", tickfont_size=13)
        st.plotly_chart(fig, width="stretch")

    with col_b:
        hdr("Tabela Comparativa de Cenários",
            "Resumo numérico dos três cenários para cada mês projetado. "
            "Use para construir o planejamento orçamentário e definir gatilhos de revisão.")
        df_show = df_pr.copy()
        df_show["receita_projetada"]    = df_show["receita_projetada"].map(fR)
        df_show["receita_otimista"]     = df_show["receita_otimista"].map(fR)
        df_show["receita_pessimista"]   = df_show["receita_pessimista"].map(fR)
        df_show["margem_projetada_pct"] = df_show["margem_projetada_pct"].map(lambda x: f"{x:.1f}%")
        # Drop seguro: errors='ignore' evita crash se mes_dt nao existir
        df_show = df_show.drop(columns=["mes_dt"], errors="ignore")
        df_show.columns = ["Mês", "Cenário Base", "Otimista", "Pessimista", "Margem (%)"]
        st.dataframe(df_show, width="stretch", hide_index=True, height=310)
