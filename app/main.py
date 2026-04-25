import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import altair as alt
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da Página
st.set_page_config(page_title="Northwind Traders | Relatório Executivo", layout="wide", page_icon="N")

# Paleta de cores pastel azul
COLORS = {
    'primary': '#4A90D9', 'secondary': '#7FB3E0', 'light': '#A8D0F0',
    'lighter': '#D4E8F7', 'bg': '#EBF3FA', 'dark': '#2C5F8A',
    'success': '#7BC5AE', 'warning': '#F0C87A', 'danger': '#E88B8B',
}
PASTEL_SCALE = alt.Scale(range=['#4A90D9','#7FB3E0','#A8D0F0','#7BC5AE','#F0C87A','#E88B8B','#B8A9C9','#F4A9A8'])

# CSS Customizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main .block-container { padding-top: 2rem; max-width: 1200px; }
    h1 { color: #2C5F8A; font-weight: 700; font-size: 1.8rem; border-bottom: 3px solid #4A90D9; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
    h2 { color: #2C5F8A; font-weight: 600; font-size: 1.3rem; margin-top: 2rem; }
    h3 { color: #2C5F8A; font-weight: 600; }
    .kpi-card {
        background: linear-gradient(135deg, #EBF3FA 0%, #D4E8F7 100%);
        border-left: 4px solid #4A90D9; border-radius: 8px;
        padding: 1.2rem 1.5rem; margin-bottom: 1rem;
    }
    .kpi-card .kpi-label { color: #5A6A7A; font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.3rem; }
    .kpi-card .kpi-value { color: #2C5F8A; font-size: 1.6rem; font-weight: 700; margin: 0; }
    .kpi-card .kpi-detail { color: #7A8A9A; font-size: 0.75rem; margin-top: 0.2rem; }
    .insight-box { background: #F7FAFD; border: 1px solid #D4E8F7; border-radius: 8px; padding: 1.2rem 1.5rem; margin: 0.8rem 0; }
    .insight-box h4 { color: #2C5F8A; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.5rem; }
    .insight-box p { color: #4A5A6A; font-size: 0.85rem; line-height: 1.6; margin: 0; }

    /* ====== REGRAS DE IMPRESSÃO (Ctrl+P / Exportar PDF) ====== */
    @media print {
        /* Remove a sidebar, toolbar e header do Streamlit */
        [data-testid="stSidebar"],
        [data-testid="stToolbar"],
        [data-testid="stHeader"],
        [data-testid="stDecoration"],
        .stDeployButton,
        #MainMenu,
        header,
        footer { display: none !important; }

        /* Força o container principal a ocupar 100% sem overflow */
        .main .block-container {
            max-width: 100% !important;
            padding: 0.5rem 1rem !important;
            margin: 0 !important;
        }
        .main, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow: visible !important;
        }

        /* Remove o scroll e garante que todo o conteúdo é visível */
        html, body {
            width: 100% !important;
            overflow: visible !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        /* Força colunas do Streamlit a empilharem verticalmente */
        [data-testid="stHorizontalBlock"],
        [data-testid="column"] {
            flex-direction: column !important;
            width: 100% !important;
            max-width: 100% !important;
            flex: 1 1 100% !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
            max-width: 100% !important;
            flex: 1 1 100% !important;
        }

        /* Gráficos Altair: força largura fixa para caber no papel */
        .vega-embed, .vega-embed svg,
        [data-testid="stVegaLiteChart"],
        [data-testid="stVegaLiteChart"] > div {
            width: 100% !important;
            max-width: 100% !important;
            overflow: visible !important;
        }

        /* Tabelas: impede overflow horizontal */
        table, [data-testid="stTable"] {
            width: 100% !important;
            max-width: 100% !important;
            font-size: 0.7rem !important;
            overflow: visible !important;
        }
        table td, table th {
            word-break: break-word !important;
            max-width: 120px !important;
            padding: 4px 6px !important;
        }

        /* Evita quebras de página dentro de elementos importantes */
        .kpi-card, .insight-box,
        .vega-embed, [data-testid="stVegaLiteChart"],
        [data-testid="stTable"],
        h1, h2, h3, h5 {
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }

        /* Força quebra de página antes de cada seção (h2) */
        h2 { page-break-before: always !important; }
        h2:first-of-type { page-break-before: avoid !important; }

        /* KPI cards: layout compacto lado a lado na impressão */
        .kpi-card {
            padding: 0.6rem 0.8rem !important;
            margin-bottom: 0.4rem !important;
        }
        .kpi-card .kpi-value { font-size: 1.2rem !important; }
        .kpi-card .kpi-label { font-size: 0.7rem !important; }

        /* Garante que as cores dos backgrounds são preservadas */
        .kpi-card, .insight-box {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        /* Reduz margens da página */
        @page {
            margin: 1cm;
            size: A4 landscape;
        }
    }
</style>
""", unsafe_allow_html=True)

# Conexão e Dados
dbUrl = os.environ.get("DATABASE_URL")
if not dbUrl:
    st.error("A variável de ambiente DATABASE_URL não foi encontrada. Verifique seu arquivo .env")
    st.stop()

@st.cache_resource
def getEngine():
    return create_engine(dbUrl)

@st.cache_data
def loadData():
    dbEngine = getEngine()
    with dbEngine.connect() as conn:
        fVendas = pd.read_sql_table('fVendas', conn)
        dClientes = pd.read_sql_table('dClientes', conn)
        fChurnClientes = pd.read_sql_table('fChurnClientes', conn)
        dProdutos = pd.read_sql_table('dProdutos', conn)
        fCesta = pd.read_sql_table('fCesta', conn)
        dFuncionarios = pd.read_sql_table('dFuncionarios', conn)
    return fVendas, dClientes, fChurnClientes, dProdutos, fCesta, dFuncionarios

def renderKpi(label, value, detail=""):
    detail_html = f'<div class="kpi-detail">{detail}</div>' if detail else ""
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{detail_html}</div>', unsafe_allow_html=True)

# Título
st.title("Northwind Traders — Relatório Executivo")

try:
    fVendas, dClientes, fChurnClientes, dProdutos, fCesta, dFuncionarios = loadData()
except Exception as e:
    st.error(f"Erro ao carregar dados do banco: {e}")
    st.stop()

# Preparar dados
fVendas['orderDate'] = pd.to_datetime(fVendas['orderDate']).dt.date
fVendas['month'] = pd.to_datetime(fVendas['orderDate']).dt.to_period('M').astype(str)
fChurnClientes['lastOrderDate'] = pd.to_datetime(fChurnClientes['lastOrderDate']).dt.date

# ==========================================================================
# SEÇÃO 1: VISÃO GERAL
# ==========================================================================
st.header("Visão Geral")

totalRevenue = fVendas['netValue'].sum()
totalOrders = fVendas['orderId'].nunique()
ticketMedio = totalRevenue / totalOrders if totalOrders > 0 else 0
totalClientes = len(fChurnClientes)
clientesChurnados = fChurnClientes['isChurn'].sum()
clientesEmRisco = len(fChurnClientes[fChurnClientes['churnStatus'] == 'Em Risco'])
churnRate = clientesChurnados / totalClientes if totalClientes > 0 else 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    renderKpi("Faturamento Total", f"US$ {totalRevenue:,.2f}", f"{totalOrders} pedidos realizados")
with k2:
    renderKpi("Ticket Médio", f"US$ {ticketMedio:,.2f}", "Faturamento / Total de pedidos")
with k3:
    renderKpi("Taxa de Churn", f"{churnRate:.1%}", f"{int(clientesChurnados)} de {totalClientes} clientes")
with k4:
    renderKpi("Clientes em Risco", f"{clientesEmRisco}", "Inativos entre 45 e 60 dias")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Receita Mensal")
    revenueByMonth = fVendas.groupby('month')['netValue'].sum().reset_index()
    revenueByMonth['label'] = (revenueByMonth['netValue'] / 1000).round(1).astype(str) + 'k'
    areaBase = alt.Chart(revenueByMonth).encode(
        x=alt.X('month:O', title='Mês', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('netValue:Q', title='Receita (US$)'),
        tooltip=[alt.Tooltip('month:O',title='Mês'), alt.Tooltip('netValue:Q',title='Receita',format=',.2f')]
    )
    areaChart = areaBase.mark_area(
        line={'color':'#4A90D9'}, color=alt.Gradient(
            gradient='linear', stops=[alt.GradientStop(color='#D4E8F7',offset=0), alt.GradientStop(color='#4A90D9',offset=1)],
            x1=1,x2=1,y1=1,y2=0
        )
    )
    areaLabels = areaBase.mark_text(dy=-12, fontSize=10, color='#2C5F8A').encode(text='label:N')
    st.altair_chart((areaChart + areaLabels).properties(height=320), use_container_width=True)

with col2:
    st.markdown("##### Top 10 Produtos por Faturamento")
    prodRev = fVendas.groupby('productId')['netValue'].sum().reset_index()
    prodRev = prodRev.merge(dProdutos, on='productId', how='left')
    top10 = prodRev.sort_values('netValue', ascending=False).head(10)
    top10['label'] = (top10['netValue'] / 1000).round(1).astype(str) + 'k'
    barProd = alt.Chart(top10).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X('netValue:Q', title='Faturamento (US$)'),
        y=alt.Y('productName:N', sort='-x', title='', axis=alt.Axis(labelLimit=250)),
        color=alt.Color('netValue:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=[alt.Tooltip('productName:N',title='Produto'), alt.Tooltip('categoryName:N',title='Categoria'), alt.Tooltip('netValue:Q',title='Faturamento',format=',.2f')]
    )
    lblProd = alt.Chart(top10).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
        x='netValue:Q', y=alt.Y('productName:N', sort='-x'), text='label:N'
    )
    st.altair_chart((barProd + lblProd).properties(height=320), use_container_width=True)

st.markdown("##### Receita por Categoria")
catRev = fVendas.merge(dProdutos[['productId','categoryName']], on='productId', how='left')
catRevAgg = catRev.groupby('categoryName')['netValue'].sum().reset_index().sort_values('netValue', ascending=False)
catRevAgg['label'] = (catRevAgg['netValue'] / 1000).round(1).astype(str) + 'k'
barCat = alt.Chart(catRevAgg).mark_bar(cornerRadiusEnd=4).encode(
    x=alt.X('netValue:Q', title='Faturamento (US$)'),
    y=alt.Y('categoryName:N', sort='-x', title='', axis=alt.Axis(labelLimit=250)),
    color=alt.Color('categoryName:N', scale=PASTEL_SCALE, legend=None),
    tooltip=[alt.Tooltip('categoryName:N',title='Categoria'), alt.Tooltip('netValue:Q',title='Faturamento',format=',.2f')]
)
lblCat = alt.Chart(catRevAgg).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
    x='netValue:Q', y=alt.Y('categoryName:N', sort='-x'), text='label:N'
)
st.altair_chart((barCat + lblCat).properties(height=280), use_container_width=True)

# ==========================================================================
# SEÇÃO 2: ANÁLISE REGIONAL
# ==========================================================================
st.header("Análise Regional")
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Faturamento por País")
    countryRev = fVendas.groupby('shipCountry')['netValue'].sum().reset_index().sort_values('netValue', ascending=False)
    top15c = countryRev.head(15).copy()
    top15c['label'] = (top15c['netValue'] / 1000).round(1).astype(str) + 'k'
    barCountry = alt.Chart(top15c).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X('netValue:Q', title='Faturamento (US$)'),
        y=alt.Y('shipCountry:N', sort='-x', title='', axis=alt.Axis(labelLimit=200)),
        color=alt.Color('netValue:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=[alt.Tooltip('shipCountry:N',title='País'), alt.Tooltip('netValue:Q',title='Faturamento',format=',.2f')]
    )
    lblCountry = alt.Chart(top15c).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
        x='netValue:Q', y=alt.Y('shipCountry:N', sort='-x'), text='label:N'
    )
    st.altair_chart((barCountry + lblCountry).properties(height=400), use_container_width=True)

with col2:
    st.markdown("##### Top 15 Cidades por Faturamento")
    cityRev = fVendas.groupby('shipCity')['netValue'].sum().reset_index().sort_values('netValue', ascending=False)
    top15city = cityRev.head(15).copy()
    top15city['label'] = (top15city['netValue'] / 1000).round(1).astype(str) + 'k'
    barCity = alt.Chart(top15city).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X('netValue:Q', title='Faturamento (US$)'),
        y=alt.Y('shipCity:N', sort='-x', title='', axis=alt.Axis(labelLimit=200)),
        color=alt.Color('netValue:Q', scale=alt.Scale(scheme='teals'), legend=None),
        tooltip=[alt.Tooltip('shipCity:N',title='Cidade'), alt.Tooltip('netValue:Q',title='Faturamento',format=',.2f')]
    )
    lblCity = alt.Chart(top15city).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
        x='netValue:Q', y=alt.Y('shipCity:N', sort='-x'), text='label:N'
    )
    st.altair_chart((barCity + lblCity).properties(height=400), use_container_width=True)

st.markdown("##### Evolução de Pedidos por País (Top 5)")
top5Countries = countryRev.head(5)['shipCountry'].tolist()
filteredOrders = fVendas[fVendas['shipCountry'].isin(top5Countries)]
ordersByCountryMonth = filteredOrders.groupby(['month','shipCountry'])['orderId'].nunique().reset_index()
chartEvolution = alt.Chart(ordersByCountryMonth).mark_line(point=True).encode(
    x=alt.X('month:O', title='Mês', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('orderId:Q', title='Pedidos'),
    color=alt.Color('shipCountry:N', scale=PASTEL_SCALE, title='País'),
    tooltip=[alt.Tooltip('month:O',title='Mês'), alt.Tooltip('shipCountry:N',title='País'), alt.Tooltip('orderId:Q',title='Pedidos')]
).properties(height=320)
st.altair_chart(chartEvolution, use_container_width=True)

# ==========================================================================
# SEÇÃO 3: ANÁLISE DE CHURN
# ==========================================================================
st.header("Análise de Churn e Retenção de Clientes")

totalClientes = len(fChurnClientes)
churnCount = len(fChurnClientes[fChurnClientes['churnStatus'] == 'Churn'])
riskCount = len(fChurnClientes[fChurnClientes['churnStatus'] == 'Em Risco'])
activeCount = len(fChurnClientes[fChurnClientes['churnStatus'] == 'Ativo'])

kc1, kc2, kc3 = st.columns(3)
with kc1:
    renderKpi("Clientes Ativos", f"{activeCount}", f"{activeCount/totalClientes:.1%} da base")
with kc2:
    renderKpi("Clientes em Risco", f"{riskCount}", "Inativos entre 45 e 60 dias")
with kc3:
    renderKpi("Clientes em Churn", f"{churnCount}", "Inativos há mais de 60 dias")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Distribuição de Status dos Clientes")
    statusDf = pd.DataFrame({'Status':['Ativo','Em Risco','Churn'], 'Quantidade':[activeCount,riskCount,churnCount]})
    statusDf['pct'] = (statusDf['Quantidade'] / statusDf['Quantidade'].sum() * 100).round(1)
    colorScale = alt.Scale(domain=['Ativo','Em Risco','Churn'], range=[COLORS['success'],COLORS['warning'],COLORS['danger']])
    arcChart = alt.Chart(statusDf).mark_arc(innerRadius=60, outerRadius=110, cornerRadius=4).encode(
        theta=alt.Theta('Quantidade:Q'),
        color=alt.Color('Status:N', scale=colorScale, legend=None),
        tooltip=['Status:N','Quantidade:Q']
    ).properties(height=280)
    st.altair_chart(arcChart, use_container_width=True)
    st.markdown(f"""
    <div style="display:flex; justify-content:center; gap:1.5rem; margin-top:-0.5rem; font-family:Inter,sans-serif; font-size:0.85rem;">
        <span><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{COLORS['success']};margin-right:5px;"></span><strong>Ativo:</strong> {activeCount} ({statusDf[statusDf['Status']=='Ativo']['pct'].values[0]}%)</span>
        <span><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{COLORS['warning']};margin-right:5px;"></span><strong>Em Risco:</strong> {riskCount} ({statusDf[statusDf['Status']=='Em Risco']['pct'].values[0]}%)</span>
        <span><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{COLORS['danger']};margin-right:5px;"></span><strong>Churn:</strong> {churnCount} ({statusDf[statusDf['Status']=='Churn']['pct'].values[0]}%)</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("##### Sazonalidade: Última Compra por Mês")
    churnDates = pd.to_datetime(fChurnClientes['lastOrderDate'])
    churnByMonth = fChurnClientes.copy()
    churnByMonth['monthPeriod'] = churnDates.dt.to_period('M').astype(str)
    churnByMonthAgg = churnByMonth.groupby('monthPeriod').agg(total=('customerId','count'), churned=('isChurn','sum')).reset_index()
    churnByMonthAgg['churnRate'] = churnByMonthAgg['churned'] / churnByMonthAgg['total']
    barSeason = alt.Chart(churnByMonthAgg).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X('monthPeriod:O', title='Mês da Última Compra', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('churned:Q', title='Clientes que deram Churn'),
        color=alt.Color('churned:Q', scale=alt.Scale(scheme='orangered'), legend=None),
        tooltip=[alt.Tooltip('monthPeriod:O',title='Mês'), alt.Tooltip('total:Q',title='Total'), alt.Tooltip('churned:Q',title='Em Churn'), alt.Tooltip('churnRate:Q',title='Taxa',format='.1%')]
    )
    lblSeason = alt.Chart(churnByMonthAgg).mark_text(dy=-10, fontSize=11, color='#2C5F8A', fontWeight='bold').encode(
        x='monthPeriod:O', y='churned:Q', text='churned:Q'
    )
    st.altair_chart((barSeason + lblSeason).properties(height=300), use_container_width=True)

st.markdown("##### Clientes em Risco (Inativos entre 45 e 60 dias)")
riskClients = fChurnClientes[fChurnClientes['churnStatus'] == 'Em Risco'].copy()
if len(riskClients) > 0:
    riskClients = riskClients.merge(dClientes, on='customerId', how='left')
    riskDisplay = riskClients[['companyName','contactName','country','city','daysSinceLastOrder','lastOrderDate']].copy()
    riskDisplay.columns = ['Empresa','Contato','País','Cidade','Dias Inativo','Última Compra']
    riskDisplay = riskDisplay.sort_values('Dias Inativo', ascending=False)
    riskDisplay['Dias Inativo'] = riskDisplay['Dias Inativo'].astype(str)
    st.table(riskDisplay.reset_index(drop=True))
else:
    st.success("Nenhum cliente na faixa de risco atualmente.")

st.markdown("##### Clientes em Churn (Inativos há mais de 60 dias)")
churnClients = fChurnClientes[fChurnClientes['churnStatus'] == 'Churn'].copy()
if len(churnClients) > 0:
    churnClients = churnClients.merge(dClientes, on='customerId', how='left')
    churnDisplay = churnClients[['companyName','contactName','country','city','daysSinceLastOrder','lastOrderDate']].copy()
    churnDisplay.columns = ['Empresa','Contato','País','Cidade','Dias Inativo','Última Compra']
    churnDisplay = churnDisplay.sort_values('Dias Inativo', ascending=False)
    churnDisplay['Dias Inativo'] = churnDisplay['Dias Inativo'].astype(str)
    st.table(churnDisplay.reset_index(drop=True))

# ==========================================================================
# SEÇÃO 4: ANÁLISE DE CESTA
# ==========================================================================
st.header("Análise de Cesta — Cross-Sell e Ticket Médio")

st.markdown("""
<div class="insight-box">
    <h4>O que é a Análise de Cesta?</h4>
    <p>A análise de cesta (Market Basket Analysis) identifica quais produtos são comprados juntos com frequência.
    Essa informação é essencial para estratégias de <strong>cross-sell</strong>: ao saber que clientes que compram
    o Produto A também compram o Produto B, podemos sugerir combos, promoções casadas e posicionamento
    estratégico para aumentar o <strong>ticket médio</strong>.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("##### Top 20 Pares de Produtos Mais Vendidos Juntos")
    top20 = fCesta.head(20).copy()
    top20['pair'] = top20['productNameA'] + '  +  ' + top20['productNameB']
    barPairs = alt.Chart(top20).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X('frequency:Q', title='Vezes comprados juntos'),
        y=alt.Y('pair:N', sort='-x', title='', axis=alt.Axis(labelLimit=400)),
        color=alt.Color('frequency:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=[
            alt.Tooltip('productNameA:N',title='Produto A'), alt.Tooltip('categoryNameA:N',title='Categoria A'),
            alt.Tooltip('productNameB:N',title='Produto B'), alt.Tooltip('categoryNameB:N',title='Categoria B'),
            alt.Tooltip('frequency:Q',title='Frequência')
        ]
    )
    lblPairs = alt.Chart(top20).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
        x='frequency:Q', y=alt.Y('pair:N', sort='-x'), text='frequency:Q'
    )
    st.altair_chart((barPairs + lblPairs).properties(height=600), use_container_width=True)

with col2:
    st.markdown("##### Cross-Sell entre Categorias")
    crossCat = fCesta.groupby(['categoryNameA','categoryNameB'])['frequency'].sum().reset_index()
    crossCat = crossCat.sort_values('frequency', ascending=False).head(15)
    crossCat['pair'] = crossCat['categoryNameA'] + '  +  ' + crossCat['categoryNameB']
    barCross = alt.Chart(crossCat).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X('frequency:Q', title='Frequência de co-ocorrência'),
        y=alt.Y('pair:N', sort='-x', title='', axis=alt.Axis(labelLimit=350)),
        color=alt.Color('frequency:Q', scale=alt.Scale(scheme='tealblues'), legend=None),
        tooltip=[alt.Tooltip('categoryNameA:N',title='Categoria A'), alt.Tooltip('categoryNameB:N',title='Categoria B'), alt.Tooltip('frequency:Q',title='Frequência')]
    )
    lblCross = alt.Chart(crossCat).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
        x='frequency:Q', y=alt.Y('pair:N', sort='-x'), text='frequency:Q'
    )
    st.altair_chart((barCross + lblCross).properties(height=600), use_container_width=True)

st.markdown("##### Ticket Médio por Categoria")
catTicket = fVendas.merge(dProdutos[['productId','categoryName']], on='productId', how='left')
catTicketAgg = catTicket.groupby('categoryName').agg(totalRevenue=('netValue','sum'), totalOrders=('orderId','nunique')).reset_index()
catTicketAgg['ticketMedio'] = catTicketAgg['totalRevenue'] / catTicketAgg['totalOrders']
catTicketAgg = catTicketAgg.sort_values('ticketMedio', ascending=False)
catTicketAgg['label'] = 'US$ ' + catTicketAgg['ticketMedio'].round(0).astype(int).astype(str)
barTicket = alt.Chart(catTicketAgg).mark_bar(cornerRadiusEnd=4).encode(
    x=alt.X('ticketMedio:Q', title='Ticket Médio (US$)'),
    y=alt.Y('categoryName:N', sort='-x', title='', axis=alt.Axis(labelLimit=250)),
    color=alt.Color('ticketMedio:Q', scale=alt.Scale(scheme='blues'), legend=None),
    tooltip=[alt.Tooltip('categoryName:N',title='Categoria'), alt.Tooltip('ticketMedio:Q',title='Ticket Médio',format=',.2f'), alt.Tooltip('totalRevenue:Q',title='Faturamento Total',format=',.2f'), alt.Tooltip('totalOrders:Q',title='Pedidos')]
)
lblTicket = alt.Chart(catTicketAgg).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
    x='ticketMedio:Q', y=alt.Y('categoryName:N', sort='-x'), text='label:N'
)
st.altair_chart((barTicket + lblTicket).properties(height=280), use_container_width=True)

# ==========================================================================
# SEÇÃO 5: ANÁLISE POR VENDEDOR
# ==========================================================================
st.header("Análise por Vendedor")

# Merge de vendas com funcionários para obter o nome do vendedor
vendasVendedor = fVendas.merge(dFuncionarios, on='employeeId', how='left')

# --- KPIs por vendedor ---
revByVendedor = vendasVendedor.groupby('fullName').agg(
    totalRevenue=('netValue', 'sum'),
    totalOrders=('orderId', 'nunique')
).reset_index()
revByVendedor['ticketMedio'] = revByVendedor['totalRevenue'] / revByVendedor['totalOrders']

# Cross-sell por vendedor: contar quantos pares de produtos distintos cada vendedor vende no mesmo pedido
from itertools import combinations
produtosPorPedido = vendasVendedor.groupby(['orderId', 'fullName'])['productId'].apply(list).reset_index()
combosList = []
for _, row in produtosPorPedido.iterrows():
    prods = sorted(set(row['productId']))
    if len(prods) >= 2:
        combosList.append({'fullName': row['fullName'], 'combos': len(list(combinations(prods, 2)))})
    else:
        combosList.append({'fullName': row['fullName'], 'combos': 0})
crossVendedor = pd.DataFrame(combosList).groupby('fullName')['combos'].sum().reset_index()
crossVendedor.columns = ['fullName', 'totalCombos']

topSeller = revByVendedor.sort_values('totalRevenue', ascending=False).iloc[0]
topTicket = revByVendedor.sort_values('ticketMedio', ascending=False).iloc[0]
topCross = crossVendedor.sort_values('totalCombos', ascending=False).iloc[0]

kv1, kv2, kv3 = st.columns(3)
with kv1:
    renderKpi("Maior Faturamento", f"US$ {topSeller['totalRevenue']:,.2f}", f"{topSeller['fullName']} — {int(topSeller['totalOrders'])} pedidos")
with kv2:
    renderKpi("Maior Ticket Médio", f"US$ {topTicket['ticketMedio']:,.2f}", f"{topTicket['fullName']}")
with kv3:
    renderKpi("Melhor Cross-Seller", f"{int(topCross['totalCombos'])} combos", f"{topCross['fullName']} — mais produtos vendidos juntos")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Faturamento por Vendedor")
    revByVendedor = revByVendedor.sort_values('totalRevenue', ascending=False)
    revByVendedor['label'] = (revByVendedor['totalRevenue'] / 1000).round(1).astype(str) + 'k'
    barRevVend = alt.Chart(revByVendedor).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X('totalRevenue:Q', title='Faturamento (US$)'),
        y=alt.Y('fullName:N', sort='-x', title='', axis=alt.Axis(labelLimit=200)),
        color=alt.Color('totalRevenue:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=[alt.Tooltip('fullName:N', title='Vendedor'), alt.Tooltip('totalRevenue:Q', title='Faturamento', format=',.2f'), alt.Tooltip('totalOrders:Q', title='Pedidos')]
    )
    lblRevVend = alt.Chart(revByVendedor).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
        x='totalRevenue:Q', y=alt.Y('fullName:N', sort='-x'), text='label:N'
    )
    st.altair_chart((barRevVend + lblRevVend).properties(height=350), use_container_width=True)

with col2:
    st.markdown("##### Ticket Médio por Vendedor")
    revByVendedor = revByVendedor.sort_values('ticketMedio', ascending=False)
    revByVendedor['labelTicket'] = 'US$ ' + revByVendedor['ticketMedio'].round(0).astype(int).astype(str)
    barTicketVend = alt.Chart(revByVendedor).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X('ticketMedio:Q', title='Ticket Médio (US$)'),
        y=alt.Y('fullName:N', sort='-x', title='', axis=alt.Axis(labelLimit=200)),
        color=alt.Color('ticketMedio:Q', scale=alt.Scale(scheme='teals'), legend=None),
        tooltip=[alt.Tooltip('fullName:N', title='Vendedor'), alt.Tooltip('ticketMedio:Q', title='Ticket Médio', format=',.2f'), alt.Tooltip('totalOrders:Q', title='Pedidos')]
    )
    lblTicketVend = alt.Chart(revByVendedor).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
        x='ticketMedio:Q', y=alt.Y('fullName:N', sort='-x'), text='labelTicket:N'
    )
    st.altair_chart((barTicketVend + lblTicketVend).properties(height=350), use_container_width=True)

st.markdown("##### Cross-Sell por Vendedor — Combos de Produtos Vendidos Juntos")
st.markdown("""
<div class="insight-box">
    <h4>Como interpretar esta análise?</h4>
    <p>O total de <strong>combos</strong> representa a soma de todos os pares de produtos distintos vendidos no mesmo pedido
    por cada vendedor. Quanto mais combos, maior a capacidade do vendedor de realizar vendas cruzadas (cross-sell),
    o que indica habilidade de sugerir produtos complementares e elevar o ticket médio.</p>
</div>
""", unsafe_allow_html=True)

crossVendedor = crossVendedor.sort_values('totalCombos', ascending=False)
crossVendedor['label'] = crossVendedor['totalCombos'].astype(str)
barCrossVend = alt.Chart(crossVendedor).mark_bar(cornerRadiusEnd=4).encode(
    x=alt.X('totalCombos:Q', title='Total de Combos de Produtos'),
    y=alt.Y('fullName:N', sort='-x', title='', axis=alt.Axis(labelLimit=200)),
    color=alt.Color('totalCombos:Q', scale=alt.Scale(scheme='purples'), legend=None),
    tooltip=[alt.Tooltip('fullName:N', title='Vendedor'), alt.Tooltip('totalCombos:Q', title='Total de Combos')]
)
lblCrossVend = alt.Chart(crossVendedor).mark_text(dx=5, align='left', fontSize=11, color='#2C5F8A').encode(
    x='totalCombos:Q', y=alt.Y('fullName:N', sort='-x'), text='label:N'
)
st.altair_chart((barCrossVend + lblCrossVend).properties(height=350), use_container_width=True)


# ==========================================================================
# SEÇÃO 6: PLANO DE AÇÃO
# ==========================================================================
st.header("Plano de Ação e Recomendações Estratégicas")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="insight-box">
        <h4>1. Aumento do Ticket Médio via Cross-Sell</h4>
        <p>A análise de cesta revelou combinações de produtos comprados juntos com alta frequência.
        Recomendamos a criação de <strong>combos promocionais</strong> baseados nos pares mais recorrentes,
        como oferecer descontos progressivos na compra de itens complementares. Categorias como
        Beverages e Dairy Products possuem forte relação de cross-sell e devem ser priorizadas
        em campanhas conjuntas. Estima-se que essa estratégia possa elevar o ticket médio em 10% a 15%.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
        <h4>2. Estratégia de Retenção e Redução de Churn</h4>
        <p>Identificamos clientes classificados como <strong>"Em Risco"</strong> (inativos entre 45 e 60 dias),
        que representam uma oportunidade concreta de retenção antes que entrem em churn definitivo.
        Recomendamos a implementação de um programa de <strong>reativação proativa</strong> com três faixas de ação:
        (a) clientes ativos recebem comunicação de fidelização; (b) clientes em risco recebem ofertas
        exclusivas com urgência; (c) clientes em churn recebem campanhas de win-back com descontos agressivos.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-box">
        <h4>3. Expansão Regional Baseada em Dados</h4>
        <p>A análise regional mostra concentração de receita em poucos mercados-chave. Recomendamos
        direcionar esforços comerciais para países com <strong>alto volume de pedidos mas ticket médio baixo</strong>,
        pois representam mercados com demanda já consolidada onde há espaço para crescimento de valor.
        Além disso, cidades que aparecem no top 15 por faturamento devem ser priorizadas para
        abertura de centros de distribuição locais, reduzindo custos de frete e tempo de entrega.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
        <h4>4. Monitoramento de Sazonalidade</h4>
        <p>A análise mensal de churn evidencia padrões sazonais na taxa de abandono de clientes.
        Períodos com picos de churn devem receber campanhas preventivas antecipadas (30 dias antes
        do início histórico da sazonalidade negativa). Além disso, meses com baixo volume de novos
        pedidos devem ser utilizados para <strong>ações de reengajamento</strong> com clientes inativos,
        aproveitando a menor concorrência por atenção para maximizar taxas de conversão.</p>
    </div>
    """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.caption("Northwind Traders | Relatório Executivo")
