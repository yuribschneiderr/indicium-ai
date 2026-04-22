import os
import pandas as pd
from pipeline.utils.db import loadToDb

def processFVendas():
    """
    Função dedicada para criar e carregar a tabela fato 'fVendas'.
    Aqui pegamos os detalhes dos pedidos, calculamos o valor líquido e padronizamos as colunas.
    """
    dataDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    # Carregando tabelas de pedidos e seus detalhes
    ordersData = pd.read_csv(os.path.join(dataDir, 'orders.csv'), sep=';', encoding='utf-8')
    orderDetailsData = pd.read_csv(os.path.join(dataDir, 'order_details.csv'), sep=';', encoding='utf-8')
    
    # Fazendo o merge (Join) de detalhes do pedido com os pedidos
    fVendas = orderDetailsData.merge(ordersData, on='order_id', how='inner')
    
    # Calculando o valor líquido: preço unitário * quantidade * (1 - desconto percentual)
    fVendas['valor_liquido'] = fVendas['unit_price'] * fVendas['quantity'] * (1 - fVendas['discount'])
    
    # Selecionando colunas relevantes
    relevantColumns = [
        'order_id', 'product_id', 'customer_id', 'employee_id', 
        'order_date', 'unit_price', 'quantity', 'discount', 'valor_liquido',
        'freight', 'ship_country'
    ]
    fVendas = fVendas[relevantColumns].copy()
    
    # Convertendo a data para um tipo de dado datetime do pandas
    fVendas['order_date'] = pd.to_datetime(fVendas['order_date'])
    
    # Padronizando o nome das colunas
    fVendas.rename(columns={
        'order_id': 'orderId',
        'product_id': 'productId',
        'customer_id': 'customerId',
        'employee_id': 'employeeId',
        'order_date': 'orderDate',
        'unit_price': 'unitPrice',
        'quantity': 'quantity',
        'discount': 'discount',
        'valor_liquido': 'netValue',  # Renomeando de valor líquido para netValue, padronizando em inglês
        'freight': 'freight',
        'ship_country': 'shipCountry'
    }, inplace=True)
    
    loadToDb(fVendas, 'fVendas')

if __name__ == '__main__':
    print("Iniciando o processamento da fato fVendas...")
    processFVendas()
