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
    assert df["mes"].min() >= "2024-01"
    assert df["mes"].max() <= "2026-04"


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
