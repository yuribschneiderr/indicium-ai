import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import altair as alt
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração inicial da página do Streamlit, com layout mais espaçado
st.set_page_config(page_title="Northwind Traders Dashboard", layout="wide", page_icon="📊")

# URL de conexão com o banco de dados Supabase
dbUrl = os.environ.get("DATABASE_URL")
if not dbUrl:
    st.error("A variável de ambiente DATABASE_URL não foi encontrada. Verifique seu arquivo .env")
    st.stop()

@st.cache_resource
def getEngine():
    """
    Cria a engine do SQLAlchemy para acessar o Supabase.
    O decorator @st.cache_resource garante que não recriaremos a conexão a cada clique.
    """
    return create_engine(dbUrl)

@st.cache_data
def loadData():
    """
    Carrega as tabelas processadas que estão no Supabase.
    As tabelas já estão devidamente modeladas via nosso ETL.
    """
    dbEngine = getEngine()
    with dbEngine.connect() as dbConnection:
        fVendas = pd.read_sql_table('fVendas', dbConnection)
        dClientes = pd.read_sql_table('dClientes', dbConnection)
        fChurnClientes = pd.read_sql_table('fChurnClientes', dbConnection)
        dProdutos = pd.read_sql_table('dProdutos', dbConnection)
    return fVendas, dClientes, fChurnClientes, dProdutos

# Título principal do dashboard
st.title("Northwind Traders Analytics - Visão Executiva 📊")

# Tentar carregar os dados com tratamento de erro amigável
try:
    fVendas, dClientes, fChurnClientes, dProdutos = loadData()
except Exception as errorMsg:
    st.error(f"Erro ao carregar dados do banco: {errorMsg}")
    st.stop()

# ==============================================================================
# KPIs (Key Performance Indicators)
# ==============================================================================

# Faturamento total: soma do valor líquido (que já tem desconto aplicado)
totalRevenue = fVendas['netValue'].sum()

# Quantidade de pedidos únicos
totalOrders = fVendas['orderId'].nunique()

# Ticket médio: faturamento total / número de pedidos
ticketMedio = totalRevenue / totalOrders if totalOrders > 0 else 0

# Taxa de churn: total de clientes churnados / total de clientes na base
totalClientes = len(fChurnClientes)
clientesChurnados = fChurnClientes['isChurn'].sum()
churnRate = clientesChurnados / totalClientes if totalClientes > 0 else 0

# Disposição dos KPIs na tela
kpiCol1, kpiCol2, kpiCol3, kpiCol4 = st.columns(4)
kpiCol1.metric("Faturamento Total", f"${totalRevenue:,.2f}")
kpiCol2.metric("Total de Pedidos", f"{totalOrders}")
kpiCol3.metric("Ticket Médio", f"${ticketMedio:,.2f}")
kpiCol4.metric("Taxa de Churn (2 meses)", f"{churnRate:.1%}")

st.divider()

# ==============================================================================
# Gráficos
# ==============================================================================

chartCol1, chartCol2 = st.columns(2)

with chartCol1:
    st.subheader("Receita por Mês")
    # Agrupa as vendas por mês
    fVendas['month'] = pd.to_datetime(fVendas['orderDate']).dt.to_period('M').astype(str)
    revenueByMonth = fVendas.groupby('month')['netValue'].sum().reset_index()
    
    # Cria gráfico de linha com o Altair
    chartRevenue = alt.Chart(revenueByMonth).mark_line(point=True).encode(
        x='month:O',
        y='netValue:Q',
        tooltip=['month', 'netValue']
    ).properties(height=300)
    st.altair_chart(chartRevenue, use_container_width=True)

with chartCol2:
    st.subheader("Situação dos Clientes (Churn vs Ativos)")
    # Calcula a quantidade de ativos vs churnados
    churnDataFrame = pd.DataFrame({
        'Status': ['Churn (> 2 meses)', 'Ativo'],
        'Quantidade': [clientesChurnados, totalClientes - clientesChurnados]
    })
    
    # Cria gráfico de arco (donut)
    chartChurn = alt.Chart(churnDataFrame).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Quantidade", type="quantitative"),
        color=alt.Color(field="Status", type="nominal", scale=alt.Scale(range=['#d62728', '#2ca02c'])),
        tooltip=['Status', 'Quantidade']
    ).properties(height=300)
    st.altair_chart(chartChurn, use_container_width=True)

st.divider()

st.subheader("Top 10 Produtos por Faturamento")
# Soma o faturamento por produto e une com a dimensão produtos para pegar o nome
productRevenue = fVendas.groupby('productId')['netValue'].sum().reset_index()
productRevenue = productRevenue.merge(dProdutos, on='productId', how='left')
# Pega os 10 mais vendidos
top10Products = productRevenue.sort_values('netValue', ascending=False).head(10)

# Gráfico de barras horizontais
chartProducts = alt.Chart(top10Products).mark_bar().encode(
    x=alt.X('netValue:Q', title='Faturamento ($)'),
    y=alt.Y('productName:N', sort='-x', title='Produto'),
    color=alt.Color('netValue:Q', scale=alt.Scale(scheme='blues'), legend=None),
    tooltip=['productName', 'categoryName', 'netValue']
).properties(height=400)

st.altair_chart(chartProducts, use_container_width=True)

# ==============================================================================
# Recomendações (Insights de Negócio)
# ==============================================================================
st.markdown("---")
st.markdown("### Recomendações e Plano de Ação")
st.info("""
**1. Aumento de Ticket Médio:**
Identificamos os produtos mais vendidos. Estratégias de *cross-selling* podem ser aplicadas oferecendo descontos nestes produtos ao adicionar itens complementares da mesma categoria.

**2. Redução de Churn:**
Uma taxa de churn acima do esperado (baseado na janela de 2 meses) aponta a necessidade de campanhas de reativação (ex: e-mail marketing, ofertas exclusivas) voltadas para clientes cujo último pedido está próximo de atingir 60 dias.
""")
