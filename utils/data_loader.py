import pandas as pd
import streamlit as st

DATA_DIR = "data"


@st.cache_data
def carregar_vendas() -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/vendas_mensais.csv")
    df["mes_dt"] = pd.to_datetime(df["mes"])
    return df


@st.cache_data
def carregar_vendedores() -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/vendedores.csv")
    df["mes_dt"] = pd.to_datetime(df["mes"])
    return df


@st.cache_data
def carregar_estoque() -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/estoque.csv")
    df["mes_dt"] = pd.to_datetime(df["mes"])
    return df


@st.cache_data
def carregar_metas() -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/metas.csv")
    df["mes_dt"] = pd.to_datetime(df["mes"])
    return df


@st.cache_data
def carregar_projecoes() -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/projecoes.csv")
    df["mes_dt"] = pd.to_datetime(df["mes"])
    return df


@st.cache_data
def carregar_catalogo() -> pd.DataFrame:
    return pd.read_csv(f"{DATA_DIR}/catalogo.csv")


def fR(valor: float) -> str:
    if abs(valor) >= 1_000_000:
        return f"R$ {valor/1_000_000:.1f}M"
    if abs(valor) >= 1_000:
        return f"R$ {valor/1_000:.0f}K"
    return f"R$ {valor:,.0f}"


def delta_pct(atual: float, anterior: float) -> float:
    if anterior == 0:
        return 0.0
    return round((atual - anterior) / anterior * 100, 1)
