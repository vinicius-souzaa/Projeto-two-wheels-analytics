"""Testes de sanidade para os dados gerados."""
import os
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

MARCAS_ESPERADAS = {"X11", "Scud", "Vessel", "HighOne", "Sentec", "WG Sports"}
COLUNAS_VENDAS   = {"mes", "sku", "produto", "marca", "categoria", "segmento",
                    "cidade", "uf", "regiao", "canal", "quantidade",
                    "receita", "custo_total", "margem_bruta"}


@pytest.fixture(scope="session", autouse=True)
def gerar_dados():
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    import generate_data  # noqa: F401


def test_vendas_existe():
    assert os.path.exists("data/vendas_mensais.csv")


def test_vendas_sem_nulos():
    df = pd.read_csv("data/vendas_mensais.csv")
    assert df.isnull().sum().sum() == 0


def test_vendas_colunas():
    df = pd.read_csv("data/vendas_mensais.csv")
    assert COLUNAS_VENDAS.issubset(set(df.columns))


def test_receita_positiva():
    df = pd.read_csv("data/vendas_mensais.csv")
    assert (df["receita"] >= 0).all()


def test_margem_coerente():
    df = pd.read_csv("data/vendas_mensais.csv")
    assert (df["margem_bruta"] <= df["receita"]).all()


def test_periodo_correto():
    df = pd.read_csv("data/vendas_mensais.csv")
    # Periodo agora vai de jan/2024 ate o dia atual (date.today())
    assert df["mes"].min() >= "2024-01"
    assert df["data"].min() >= "2024-01-01"
    # nao deve haver data no futuro
    import datetime as _dt
    hoje = _dt.date.today().strftime("%Y-%m-%d")
    assert df["data"].max() <= hoje, f"Existe data futura no dataset: {df['data'].max()} > {hoje}"


def test_todas_marcas_presentes():
    df = pd.read_csv("data/vendas_mensais.csv")
    assert MARCAS_ESPERADAS.issubset(set(df["marca"].unique()))


def test_cidades_nacionais():
    df = pd.read_csv("data/vendas_mensais.csv")
    regioes = set(df["regiao"].unique())
    assert {"Sul", "Sudeste", "Nordeste", "Centro-Oeste", "Norte"}.issubset(regioes)


def test_catalogo_marcas():
    df = pd.read_csv("data/catalogo.csv")
    assert MARCAS_ESPERADAS == set(df["marca"].unique())


def test_sem_categoria_vestuario():
    df = pd.read_csv("data/catalogo.csv")
    assert "Vestuario" not in df["categoria"].values, "Categoria 'Vestuario' nao deve existir"


def test_canal_sem_loja_fisica():
    df = pd.read_csv("data/vendas_mensais.csv")
    assert "Loja Fisica" not in df["canal"].values, "Canal 'Loja Fisica' deve ser 'Varejo Fisico'"


def test_metas_existe():
    assert os.path.exists("data/metas.csv")


def test_projecoes_periodo():
    df = pd.read_csv("data/projecoes.csv")
    assert df["mes"].min() == "2026-05"
    assert df["mes"].max() == "2026-10"


def test_data_loader():
    from utils.data_loader import fR, delta_pct
    assert fR(1_500_000) == "R$ 1.5M"
    assert fR(42_000)    == "R$ 42K"
    assert delta_pct(110, 100) == 10.0
    assert delta_pct(90, 100)  == -10.0


# ── Testes para bugs corrigidos ──────────────────────────────────────────────
def test_bug5_sem_linhas_quantidade_zero():
    """Bug #5: dataset nao deve ter linhas com quantidade=0 (eram 76% antes)."""
    df = pd.read_csv("data/vendas_mensais.csv")
    assert (df["quantidade"] > 0).all(), "Existem linhas com quantidade<=0"


def test_bug4_vendedores_reconciliam_com_vendas():
    """Bug #4: receita de vendedores deve casar com vendas por mes."""
    df_v = pd.read_csv("data/vendas_mensais.csv")
    df_ve = pd.read_csv("data/vendedores.csv")
    rec_vendas = df_v.groupby("mes")["receita"].sum()
    rec_vended = df_ve.groupby("mes")["receita_realizada"].sum()
    # Tolerancia de R$ 5 por mes (arredondamento de 8 vendedores)
    diff = (rec_vendas - rec_vended).abs()
    assert (diff < 5).all(), f"Diferenca alem do esperado: {diff[diff>=5].to_dict()}"


def test_bug10_vendedores_tem_regiao():
    """Bug #10: vendedores devem ter coluna regiao_atuacao."""
    df_ve = pd.read_csv("data/vendedores.csv")
    assert "regiao_atuacao" in df_ve.columns
    regioes_validas = {"Sul", "Sudeste", "Nordeste", "Centro-Oeste", "Norte"}
    assert set(df_ve["regiao_atuacao"].unique()).issubset(regioes_validas)


def test_bug1_metas_canal_existe():
    """Bug #1: arquivo metas_canal.csv deve existir e ter 4 canais."""
    assert os.path.exists("data/metas_canal.csv")
    df = pd.read_csv("data/metas_canal.csv")
    assert set(df["canal"].unique()) == {"Varejo Fisico", "E-commerce",
                                          "Distribuidores", "Marketplace"}


def test_vendas_tem_coluna_data():
    """Vendas com granularidade diaria — coluna 'data' obrigatoria."""
    df = pd.read_csv("data/vendas_mensais.csv")
    assert "data" in df.columns
    # data deve ser parseavel como YYYY-MM-DD
    parsed = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    assert parsed.notna().all(), "Existem datas em formato invalido"
    # deve haver mais de um dia distinto por mes (granularidade real)
    df["data_dt"] = parsed
    dias_por_mes = df.groupby("mes")["data_dt"].nunique()
    assert (dias_por_mes > 1).any(), "Granularidade diaria nao foi aplicada"
