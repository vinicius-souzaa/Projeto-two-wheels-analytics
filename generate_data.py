"""
Gerador de dados sinteticos para dashboard LM 2 Rodas.
Periodo: janeiro/2024 a abril/2026.
Marcas: X11, Scud, Sentec, HighOne, WG Sports, Vessel.
Produtos baseados no portfolio real das marcas do grupo.
Cidades: cobertura nacional (Sul, Sudeste, CO, Norte, Nordeste).
"""
import os
import numpy as np
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

np.random.seed(42)
os.makedirs("data", exist_ok=True)

# ── Catalogo de produtos reais das marcas LM 2 Rodas ─────────────────────────
# Margens-alvo por marca (diferenciam claramente no grafico):
#   WG Sports ~65%  |  Vessel ~62%  |  X11 ~57%
#   Scud ~52%       |  HighOne ~47% |  Sentec ~42%
MARGEM_MARCA = {
    "X11":       0.43,   # custo = 43% do preco -> margem 57%
    "Scud":      0.48,   # custo = 48% do preco -> margem 52%
    "Vessel":    0.38,   # custo = 38% do preco -> margem 62%
    "HighOne":   0.53,   # custo = 53% do preco -> margem 47%
    "Sentec":    0.58,   # custo = 58% do preco -> margem 42%
    "WG Sports": 0.35,   # custo = 35% do preco -> margem 65%
}

def _c(marca, preco):
    """Calcula custo com base na margem-alvo da marca."""
    return round(preco * MARGEM_MARCA[marca], 2)

PRODUTOS = [
    # ── X11 | Capacetes ──────────────────────────────────────────────────────
    {"sku": "X11-CAP-001", "nome": "Capacete X11 Trust Pro Transit",     "marca": "X11",       "categoria": "Capacetes",   "segmento": "Moto", "preco": 449.90, "custo": _c("X11",       449.90)},
    {"sku": "X11-CAP-002", "nome": "Capacete X11 Trust Pro 11",          "marca": "X11",       "categoria": "Capacetes",   "segmento": "Moto", "preco": 499.90, "custo": _c("X11",       499.90)},
    {"sku": "X11-CAP-003", "nome": "Capacete X11 Revo Pro Flagger",      "marca": "X11",       "categoria": "Capacetes",   "segmento": "Moto", "preco": 649.90, "custo": _c("X11",       649.90)},
    {"sku": "X11-CAP-004", "nome": "Capacete X11 Revo Pro All Black",    "marca": "X11",       "categoria": "Capacetes",   "segmento": "Moto", "preco": 749.90, "custo": _c("X11",       749.90)},
    {"sku": "X11-CAP-005", "nome": "Capacete X11 Turner SV Articulado",  "marca": "X11",       "categoria": "Capacetes",   "segmento": "Moto", "preco": 899.90, "custo": _c("X11",       899.90)},
    {"sku": "X11-CAP-006", "nome": "Capacete X11 Crossover Off Road",    "marca": "X11",       "categoria": "Capacetes",   "segmento": "Moto", "preco": 999.90, "custo": _c("X11",       999.90)},
    {"sku": "X11-CAP-007", "nome": "Capacete X11 Ghost Urban",           "marca": "X11",       "categoria": "Capacetes",   "segmento": "Moto", "preco": 579.90, "custo": _c("X11",       579.90)},
    # ── X11 | Jaquetas ───────────────────────────────────────────────────────
    {"sku": "X11-JAQ-001", "nome": "Jaqueta X11 Iron 3 Sporadic",        "marca": "X11",       "categoria": "Jaquetas",    "segmento": "Moto", "preco": 449.90, "custo": _c("X11",       449.90)},
    {"sku": "X11-JAQ-002", "nome": "Jaqueta X11 Super Air Ventilada",    "marca": "X11",       "categoria": "Jaquetas",    "segmento": "Moto", "preco": 399.90, "custo": _c("X11",       399.90)},
    {"sku": "X11-JAQ-003", "nome": "Jaqueta X11 Breeze 2 Ventilada",     "marca": "X11",       "categoria": "Jaquetas",    "segmento": "Moto", "preco": 349.90, "custo": _c("X11",       349.90)},
    {"sku": "X11-JAQ-004", "nome": "Jaqueta X11 Expedition Impermeavel", "marca": "X11",       "categoria": "Jaquetas",    "segmento": "Moto", "preco": 599.90, "custo": _c("X11",       599.90)},
    {"sku": "X11-JAQ-005", "nome": "Jaqueta X11 One Sport Masculina",    "marca": "X11",       "categoria": "Jaquetas",    "segmento": "Moto", "preco": 299.90, "custo": _c("X11",       299.90)},
    {"sku": "X11-JAQ-006", "nome": "Jaqueta X11 Sport Naked",            "marca": "X11",       "categoria": "Jaquetas",    "segmento": "Moto", "preco": 329.90, "custo": _c("X11",       329.90)},
    # ── X11 | Luvas ──────────────────────────────────────────────────────────
    {"sku": "X11-LUV-001", "nome": "Luva X11 Route 2 Couro",             "marca": "X11",       "categoria": "Luvas",       "segmento": "Moto", "preco": 189.90, "custo": _c("X11",       189.90)},
    {"sku": "X11-LUV-002", "nome": "Luva X11 Blackout 2",                "marca": "X11",       "categoria": "Luvas",       "segmento": "Moto", "preco": 129.90, "custo": _c("X11",       129.90)},
    {"sku": "X11-LUV-003", "nome": "Luva X11 Impact 2 Cano Longo",       "marca": "X11",       "categoria": "Luvas",       "segmento": "Moto", "preco": 229.90, "custo": _c("X11",       229.90)},
    {"sku": "X11-LUV-004", "nome": "Luva X11 Thermic Segunda Pele",      "marca": "X11",       "categoria": "Luvas",       "segmento": "Moto", "preco": 89.90,  "custo": _c("X11",        89.90)},
    {"sku": "X11-LUV-005", "nome": "Luva X11 Nitro 4",                   "marca": "X11",       "categoria": "Luvas",       "segmento": "Moto", "preco": 139.90, "custo": _c("X11",       139.90)},
    # ── X11 | Calcas e Botas ─────────────────────────────────────────────────
    {"sku": "X11-CAL-001", "nome": "Calca X11 Montano Masculina",        "marca": "X11",       "categoria": "Calcas",      "segmento": "Moto", "preco": 349.90, "custo": _c("X11",       349.90)},
    {"sku": "X11-CAL-002", "nome": "Calca X11 Urban Feminina",           "marca": "X11",       "categoria": "Calcas",      "segmento": "Moto", "preco": 299.90, "custo": _c("X11",       299.90)},
    {"sku": "X11-BOT-001", "nome": "Bota X11 Urban 2",                   "marca": "X11",       "categoria": "Botas",       "segmento": "Moto", "preco": 399.90, "custo": _c("X11",       399.90)},
    {"sku": "X11-BOT-002", "nome": "Bota X11 Dirt Trilha",               "marca": "X11",       "categoria": "Botas",       "segmento": "Moto", "preco": 549.90, "custo": _c("X11",       549.90)},
    # ── Scud | Capacetes ─────────────────────────────────────────────────────
    {"sku": "SCD-CAP-001", "nome": "Capacete Scud Fenix Solide",         "marca": "Scud",      "categoria": "Capacetes",   "segmento": "Moto", "preco": 349.90, "custo": _c("Scud",      349.90)},
    {"sku": "SCD-CAP-002", "nome": "Capacete Scud Attack 2 Viseira",     "marca": "Scud",      "categoria": "Capacetes",   "segmento": "Moto", "preco": 279.90, "custo": _c("Scud",      279.90)},
    {"sku": "SCD-CAP-003", "nome": "Capacete Scud E-Future Eletrico",    "marca": "Scud",      "categoria": "Capacetes",   "segmento": "Moto", "preco": 499.90, "custo": _c("Scud",      499.90)},
    {"sku": "SCD-CAP-004", "nome": "Capacete Scud Speed Carbon",         "marca": "Scud",      "categoria": "Capacetes",   "segmento": "Moto", "preco": 599.90, "custo": _c("Scud",      599.90)},
    # ── Scud | Acessorios ────────────────────────────────────────────────────
    {"sku": "SCD-ACE-001", "nome": "Viseira Scud Fume Universal",        "marca": "Scud",      "categoria": "Acessorios",  "segmento": "Moto", "preco": 79.90,  "custo": _c("Scud",       79.90)},
    {"sku": "SCD-ACE-002", "nome": "Bagageiro Scud Universal Moto",      "marca": "Scud",      "categoria": "Acessorios",  "segmento": "Moto", "preco": 149.90, "custo": _c("Scud",      149.90)},
    {"sku": "SCD-ACE-003", "nome": "Capa de Chuva Scud Moto",            "marca": "Scud",      "categoria": "Acessorios",  "segmento": "Moto", "preco": 59.90,  "custo": _c("Scud",       59.90)},
    {"sku": "SCD-ACE-004", "nome": "Antena Scud Curta Universal",        "marca": "Scud",      "categoria": "Acessorios",  "segmento": "Moto", "preco": 29.90,  "custo": _c("Scud",       29.90)},
    {"sku": "SCD-ACE-005", "nome": "Spoiler Traseiro Scud Honda CG",     "marca": "Scud",      "categoria": "Acessorios",  "segmento": "Moto", "preco": 89.90,  "custo": _c("Scud",       89.90)},
    # ── Vessel | Vestuario e protecao moto ───────────────────────────────────
    {"sku": "VES-JAQ-001", "nome": "Jaqueta Vessel Basic Urban",         "marca": "Vessel",    "categoria": "Jaquetas",    "segmento": "Moto", "preco": 259.90, "custo": _c("Vessel",    259.90)},
    {"sku": "VES-CAL-001", "nome": "Calca Vessel Urban Stretch",         "marca": "Vessel",    "categoria": "Calcas",      "segmento": "Moto", "preco": 299.90, "custo": _c("Vessel",    299.90)},
    {"sku": "VES-LUV-001", "nome": "Luva Vessel Street Ventilada",       "marca": "Vessel",    "categoria": "Luvas",       "segmento": "Moto", "preco": 119.90, "custo": _c("Vessel",    119.90)},
    {"sku": "VES-CAP-001", "nome": "Capacete Vessel Integral Full",      "marca": "Vessel",    "categoria": "Capacetes",   "segmento": "Moto", "preco": 319.90, "custo": _c("Vessel",    319.90)},
    {"sku": "VES-ACE-001", "nome": "Kit Protecao Vessel Joelhos/Cotovelo","marca": "Vessel",   "categoria": "Acessorios",  "segmento": "Moto", "preco": 149.90, "custo": _c("Vessel",    149.90)},
    # ── HighOne | Bicicletas ─────────────────────────────────────────────────
    {"sku": "HO-BIK-001",  "nome": "Bike HighOne Attack Sport 21v Aro 29","marca": "HighOne",  "categoria": "Bicicletas",  "segmento": "Bike", "preco": 1499.00,"custo": _c("HighOne",  1499.00)},
    {"sku": "HO-BIK-002",  "nome": "Bike HighOne MTB Expert 24v Aro 29", "marca": "HighOne",  "categoria": "Bicicletas",  "segmento": "Bike", "preco": 2299.00,"custo": _c("HighOne",  2299.00)},
    {"sku": "HO-BIK-003",  "nome": "Bike HighOne Speed React 700c",      "marca": "HighOne",  "categoria": "Bicicletas",  "segmento": "Bike", "preco": 2899.00,"custo": _c("HighOne",  2899.00)},
    {"sku": "HO-BIK-004",  "nome": "Bike HighOne Kids Fun 20v",          "marca": "HighOne",  "categoria": "Bicicletas",  "segmento": "Bike", "preco": 799.00, "custo": _c("HighOne",   799.00)},
    # ── HighOne | Acessorios bike ────────────────────────────────────────────
    {"sku": "HO-ACE-001",  "nome": "Capacete HighOne MTB Trail",         "marca": "HighOne",  "categoria": "Capacetes",   "segmento": "Bike", "preco": 199.90, "custo": _c("HighOne",   199.90)},
    {"sku": "HO-ACE-002",  "nome": "Luva HighOne Trail Gel",             "marca": "HighOne",  "categoria": "Luvas",       "segmento": "Bike", "preco": 89.90,  "custo": _c("HighOne",    89.90)},
    {"sku": "HO-ACE-003",  "nome": "Oculos HighOne Vision UV400",        "marca": "HighOne",  "categoria": "Acessorios",  "segmento": "Bike", "preco": 129.90, "custo": _c("HighOne",   129.90)},
    {"sku": "HO-ACE-004",  "nome": "Camiseta HighOne Dry-Fit Ciclismo",  "marca": "HighOne",  "categoria": "Acessorios",  "segmento": "Bike", "preco": 79.90,  "custo": _c("HighOne",    79.90)},
    # ── Sentec | Rodas e componentes bike ────────────────────────────────────
    {"sku": "SEN-ROD-001", "nome": "Roda Sentec Aero 30 Road Alu",       "marca": "Sentec",   "categoria": "Rodas",       "segmento": "Bike", "preco": 799.00, "custo": _c("Sentec",    799.00)},
    {"sku": "SEN-ROD-002", "nome": "Roda Sentec Aero 50 Carbon Road",    "marca": "Sentec",   "categoria": "Rodas",       "segmento": "Bike", "preco": 2499.00,"custo": _c("Sentec",   2499.00)},
    {"sku": "SEN-ROD-003", "nome": "Roda Sentec Comp 29 MTB",            "marca": "Sentec",   "categoria": "Rodas",       "segmento": "Bike", "preco": 549.00, "custo": _c("Sentec",    549.00)},
    {"sku": "SEN-ROD-004", "nome": "Roda Sentec Trail 29 MTB Tubeless",  "marca": "Sentec",   "categoria": "Rodas",       "segmento": "Bike", "preco": 699.00, "custo": _c("Sentec",    699.00)},
    # ── WG Sports | Componentes bike ─────────────────────────────────────────
    {"sku": "WGS-CUB-001", "nome": "Cubo Traseiro WG Sports Disco 36F",  "marca": "WG Sports","categoria": "Componentes",  "segmento": "Bike", "preco": 89.00,  "custo": _c("WG Sports",  89.00)},
    {"sku": "WGS-CUB-002", "nome": "Cubo Dianteiro WG Sports Disco 32F", "marca": "WG Sports","categoria": "Componentes",  "segmento": "Bike", "preco": 69.00,  "custo": _c("WG Sports",  69.00)},
    {"sku": "WGS-ROL-001", "nome": "Roldana Cambio WG Sports Alu 11d",   "marca": "WG Sports","categoria": "Componentes",  "segmento": "Bike", "preco": 39.00,  "custo": _c("WG Sports",  39.00)},
    {"sku": "WGS-KIT-001", "nome": "Kit Cubo WG Sports Completo",        "marca": "WG Sports","categoria": "Componentes",  "segmento": "Bike", "preco": 149.00, "custo": _c("WG Sports", 149.00)},
]

# ── Cidades nacionais ─────────────────────────────────────────────────────────
CIDADES = [
    # Sul
    ("Curitiba",          "PR", "Sul"),
    ("Londrina",          "PR", "Sul"),
    ("Maringa",           "PR", "Sul"),
    ("Cascavel",          "PR", "Sul"),
    ("Ponta Grossa",      "PR", "Sul"),
    ("Foz do Iguacu",     "PR", "Sul"),
    ("Porto Alegre",      "RS", "Sul"),
    ("Caxias do Sul",     "RS", "Sul"),
    ("Florianopolis",     "SC", "Sul"),
    ("Joinville",         "SC", "Sul"),
    # Sudeste
    ("Sao Paulo",         "SP", "Sudeste"),
    ("Campinas",          "SP", "Sudeste"),
    ("Ribeirao Preto",    "SP", "Sudeste"),
    ("Rio de Janeiro",    "RJ", "Sudeste"),
    ("Belo Horizonte",    "MG", "Sudeste"),
    ("Nova Lima",         "MG", "Sudeste"),
    ("Vitoria",           "ES", "Sudeste"),
    # Centro-Oeste
    ("Brasilia",          "DF", "Centro-Oeste"),
    ("Goiania",           "GO", "Centro-Oeste"),
    ("Campo Grande",      "MS", "Centro-Oeste"),
    ("Cuiaba",            "MT", "Centro-Oeste"),
    # Nordeste
    ("Salvador",          "BA", "Nordeste"),
    ("Fortaleza",         "CE", "Nordeste"),
    ("Recife",            "PE", "Nordeste"),
    ("Natal",             "RN", "Nordeste"),
    ("Maceio",            "AL", "Nordeste"),
    # Norte
    ("Manaus",            "AM", "Norte"),
    ("Belem",             "PA", "Norte"),
]

NOMES_CIDADES = [c[0] for c in CIDADES]
PESOS_REGIAO = {
    "Sul":          0.28,
    "Sudeste":      0.38,
    "Centro-Oeste": 0.14,
    "Nordeste":     0.13,
    "Norte":        0.07,
}

def peso_cidade(cidade_tuple):
    regiao = cidade_tuple[2]
    n_cidades_regiao = sum(1 for c in CIDADES if c[2] == regiao)
    return PESOS_REGIAO[regiao] / n_cidades_regiao

PESOS_CIDADES = [peso_cidade(c) for c in CIDADES]

CANAIS = ["Varejo Fisico", "E-commerce", "Distribuidores", "Marketplace"]
PESOS_CANAL = [0.25, 0.38, 0.22, 0.15]

VENDEDORES = [
    "Ana Paula Ferreira",
    "Carlos Eduardo Lima",
    "Fernanda Oliveira",
    "Ricardo Souza",
    "Juliana Costa",
    "Marcos Vieira",
    "Patricia Mendes",
    "Diego Alves",
]

# sazonalidade mensal (pico nov/dez, julho, e agosto)
SAZONALIDADE = np.array([
    0.82, 0.79, 0.85, 0.88, 0.91, 0.95,
    1.12, 1.04, 0.97, 1.05, 1.18, 1.24
])

START = date(2024, 1, 1)
END   = date(2026, 4, 30)


def meses_entre(inicio, fim):
    datas, atual = [], inicio.replace(day=1)
    while atual <= fim.replace(day=1):
        datas.append(atual)
        atual += relativedelta(months=1)
    return datas


MESES = meses_entre(START, END)
N_MESES = len(MESES)
# crescimento mensal ~18% a.a. = ~1.4% ao mes
CRESCIMENTO = np.array([(1.014) ** i for i in range(N_MESES)])


# ── 1. Vendas mensais ─────────────────────────────────────────────────────────
def gerar_vendas():
    rows = []
    for idx, mes in enumerate(MESES):
        saz   = SAZONALIDADE[mes.month - 1]
        cresc = CRESCIMENTO[idx]
        for prod in PRODUTOS:
            # base por faixa de preco
            if prod["preco"] < 100:
                lam_base = 60
            elif prod["preco"] < 300:
                lam_base = 30
            elif prod["preco"] < 700:
                lam_base = 14
            elif prod["preco"] < 1500:
                lam_base = 6
            else:
                lam_base = 3

            for i_cid, (cidade, uf, regiao) in enumerate(CIDADES):
                for canal, pc in zip(CANAIS, PESOS_CANAL):
                    qtd = max(0, int(round(
                        np.random.poisson(lam_base) *
                        PESOS_CIDADES[i_cid] * pc * saz * cresc *
                        np.random.uniform(0.65, 1.35)
                    )))
                    if qtd == 0 and np.random.random() > 0.55:
                        continue
                    desc = np.random.choice(
                        [0, 0, 0, 0.05, 0.08, 0.10, 0.12],
                        p=[0.50, 0.15, 0.10, 0.10, 0.07, 0.05, 0.03]
                    )
                    pv = round(prod["preco"] * (1 - desc), 2)
                    rows.append({
                        "mes":            mes.strftime("%Y-%m"),
                        "sku":            prod["sku"],
                        "produto":        prod["nome"],
                        "marca":          prod["marca"],
                        "categoria":      prod["categoria"],
                        "segmento":       prod["segmento"],
                        "cidade":         cidade,
                        "uf":             uf,
                        "regiao":         regiao,
                        "canal":          canal,
                        "quantidade":     qtd,
                        "preco_unitario": pv,
                        "custo_unitario": prod["custo"],
                        "receita":        round(qtd * pv, 2),
                        "custo_total":    round(qtd * prod["custo"], 2),
                        "margem_bruta":   round(qtd * (pv - prod["custo"]), 2),
                    })
    df = pd.DataFrame(rows)
    df.to_csv("data/vendas_mensais.csv", index=False)
    print(f"  vendas_mensais.csv -> {len(df):,} linhas | R$ {df['receita'].sum():,.0f} total")
    return df


# ── 2. Vendedores ─────────────────────────────────────────────────────────────
def gerar_vendedores(df_v):
    rows = []
    for mes in MESES:
        mes_str = mes.strftime("%Y-%m")
        rec_mes = df_v[df_v["mes"] == mes_str]["receita"].sum()
        shares  = np.random.dirichlet(np.ones(len(VENDEDORES)) * 3)
        for vend, share in zip(VENDEDORES, shares):
            receita = round(rec_mes * share * np.random.uniform(0.88, 1.12), 2)
            meta    = round(receita * np.random.uniform(0.90, 1.18), 2)
            clientes = np.random.randint(25, 90)
            rows.append({
                "mes":               mes_str,
                "vendedor":          vend,
                "receita_realizada": receita,
                "meta_receita":      meta,
                "atingimento_pct":   round(receita / meta * 100, 1),
                "clientes_atendidos":clientes,
                "ticket_medio":      round(receita / clientes, 2),
            })
    df = pd.DataFrame(rows)
    df.to_csv("data/vendedores.csv", index=False)
    print(f"  vendedores.csv      -> {len(df):,} linhas")
    return df


# ── 3. Estoque ────────────────────────────────────────────────────────────────
def gerar_estoque(df_v):
    rows = []
    for mes in MESES:
        mes_str = mes.strftime("%Y-%m")
        for prod in PRODUTOS:
            vendido = int(df_v[(df_v["mes"] == mes_str) &
                               (df_v["sku"] == prod["sku"])]["quantidade"].sum())
            estoque = max(0, int(vendido * np.random.uniform(0.7, 2.2)))
            rows.append({
                "mes":             mes_str,
                "sku":             prod["sku"],
                "produto":         prod["nome"],
                "marca":           prod["marca"],
                "categoria":       prod["categoria"],
                "segmento":        prod["segmento"],
                "estoque_unidades":estoque,
                "estoque_valor":   round(estoque * prod["custo"], 2),
                "vendido_mes":     vendido,
                "giro_estoque":    round(vendido / max(1, estoque), 2),
                "cobertura_dias":  int(round(estoque / max(1, vendido) * 30)),
            })
    df = pd.DataFrame(rows)
    df.to_csv("data/estoque.csv", index=False)
    print(f"  estoque.csv         -> {len(df):,} linhas")
    return df


# ── 4. Metas vs realizado por marca ──────────────────────────────────────────
def gerar_metas(df_v):
    """
    Gera metas com distribuicao realista: ~45% bom (verde), ~30% neutro,
    ~25% ruim (vermelho). A meta e definida no nivel do mes (mesmo tipo
    para todas as marcas naquele mes), simulando um planejamento top-down
    que erra para cima ou para baixo dependendo do cenario de mercado.
    """
    marcas = ["X11", "Scud", "Vessel", "HighOne", "Sentec", "WG Sports"]
    rows   = []
    for mes in MESES:
        mes_str = mes.strftime("%Y-%m")
        # tipo do mes e definido uma vez para refletir cenario macro comum
        mes_tipo = np.random.choice(
            ["bom", "neutro", "ruim"],
            p=[0.45, 0.30, 0.25]
        )
        for marca in marcas:
            real = df_v[(df_v["mes"] == mes_str) &
                        (df_v["marca"] == marca)]["receita"].sum()
            # bounds garantem que bom -> verde, ruim -> vermelho no grafico
            if mes_tipo == "bom":
                bounds = (0.86, 0.96)   # meta abaixo do real  -> verde
            elif mes_tipo == "neutro":
                bounds = (0.97, 1.04)   # proximo de zero      -> amarelo/leve
            else:
                bounds = (1.05, 1.17)   # meta acima do real   -> vermelho
            # variacao individual por marca (+/- 3 pp) para nao ficarem identicas
            lo = max(0.70, bounds[0] + np.random.uniform(-0.03, 0.02))
            hi = bounds[1] + np.random.uniform(-0.02, 0.03)
            meta = round(real * np.random.uniform(lo, hi), 2)
            qtd  = int(df_v[(df_v["mes"] == mes_str) &
                            (df_v["marca"] == marca)]["quantidade"].sum())
            mg   = df_v[(df_v["mes"] == mes_str) &
                        (df_v["marca"] == marca)]["margem_bruta"].sum()
            rows.append({
                "mes":               mes_str,
                "marca":             marca,
                "receita_realizada": round(real, 2),
                "meta_receita":      meta,
                "variacao_pct":      round((real - meta) / max(1, meta) * 100, 1),
                "unidades_vendidas": qtd,
                "margem_bruta":      round(mg, 2),
            })
    df = pd.DataFrame(rows)
    df.to_csv("data/metas.csv", index=False)
    print(f"  metas.csv           -> {len(df):,} linhas")
    return df


# ── 5. Projecoes (mai-out 2026) ───────────────────────────────────────────────
def gerar_projecoes(df_v):
    base = df_v[df_v["mes"] == df_v["mes"].max()]["receita"].sum()
    rows = []
    for i in range(6):
        mes_proj = date(2026, 5, 1) + relativedelta(months=i)
        saz  = SAZONALIDADE[mes_proj.month - 1]
        rows.append({
            "mes":                mes_proj.strftime("%Y-%m"),
            "receita_projetada":  round(base * saz * (1.014) ** (i + 1), 2),
            "receita_otimista":   round(base * saz * (1.025) ** (i + 1), 2),
            "receita_pessimista": round(base * saz * (1.005) ** (i + 1), 2),
            "margem_projetada_pct": round(np.random.uniform(37, 45), 1),
        })
    df = pd.DataFrame(rows)
    df.to_csv("data/projecoes.csv", index=False)
    print(f"  projecoes.csv       -> {len(df):,} linhas")
    return df


# ── 6. Catalogo ───────────────────────────────────────────────────────────────
def gerar_catalogo():
    df = pd.DataFrame(PRODUTOS)
    df["margem_pct"] = round((df["preco"] - df["custo"]) / df["preco"] * 100, 1)
    df.to_csv("data/catalogo.csv", index=False)
    print(f"  catalogo.csv        -> {len(df):,} produtos | {df['marca'].nunique()} marcas")
    return df


if __name__ == "__main__":
    print("Gerando dados LM 2 Rodas (jan/2024 - abr/2026)...\n")
    df_v = gerar_vendas()
    gerar_vendedores(df_v)
    gerar_estoque(df_v)
    gerar_metas(df_v)
    gerar_projecoes(df_v)
    gerar_catalogo()
    print("\nConcluido com sucesso em ./data/")
