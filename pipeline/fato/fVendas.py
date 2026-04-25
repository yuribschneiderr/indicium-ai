import os
import pandas as pd
from pipeline.utils.db import loadToDb

def processFVendas():
    """
    Função dedicada para criar e carregar a tabela fato 'fVendas'.
    Aqui pegar os detalhes dos pedidos, calcular o valor líquido e padronizar as colunas.
    """
    dataDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    # Carregar tabelas de pedidos e seus detalhes
    ordersData = pd.read_csv(os.path.join(dataDir, 'orders.csv'), sep=';', encoding='utf-8')
    orderDetailsData = pd.read_csv(os.path.join(dataDir, 'order_details.csv'), sep=';', encoding='utf-8')
    
    # Fazer o merge (Join) de detalhes do pedido com os pedidos
    fVendas = orderDetailsData.merge(ordersData, on='order_id', how='inner')
    
    # Calcular o valor líquido: preço unitário * quantidade * (1 - desconto percentual)
    fVendas['valor_liquido'] = fVendas['unit_price'] * fVendas['quantity'] * (1 - fVendas['discount'])
    
    # Selecionar colunas relevantes (incluindo dados regionais e datas de entrega)
    relevantColumns = [
        'order_id', 'product_id', 'customer_id', 'employee_id', 
        'order_date', 'required_date', 'shipped_date',
        'unit_price', 'quantity', 'discount', 'valor_liquido',
        'freight', 'ship_city', 'ship_region', 'ship_country'
    ]
    fVendas = fVendas[relevantColumns].copy()
    
    # Converter as datas para tipo datetime do pandas
    fVendas['order_date'] = pd.to_datetime(fVendas['order_date'])
    fVendas['required_date'] = pd.to_datetime(fVendas['required_date'])
    fVendas['shipped_date'] = pd.to_datetime(fVendas['shipped_date'])
    
    # Padronizar o nome das colunas
    fVendas.rename(columns={
        'order_id': 'orderId',
        'product_id': 'productId',
        'customer_id': 'customerId',
        'employee_id': 'employeeId',
        'order_date': 'orderDate',
        'required_date': 'requiredDate',
        'shipped_date': 'shippedDate',
        'unit_price': 'unitPrice',
        'quantity': 'quantity',
        'discount': 'discount',
        'valor_liquido': 'netValue',  # Renomear de valor líquido para netValue, padronizar em inglês
        'freight': 'freight',
        'ship_city': 'shipCity',
        'ship_region': 'shipRegion',
        'ship_country': 'shipCountry'
    }, inplace=True)
    
    loadToDb(fVendas, 'fVendas')

if __name__ == '__main__':
    print("Iniciando o processamento da fato fVendas...")
    processFVendas()
