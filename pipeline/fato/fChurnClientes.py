import os
import pandas as pd
from pipeline.utils.db import loadToDb

def processFChurnClientes():
    """
    Função dedicada para criar e carregar a tabela fato (ou tabela derivada) 'fChurnClientes'.
    Aqui nós verificamos a última compra do cliente e calculamos se ele deu Churn
    baseado na regra de 2 meses sem comprar (60 dias).
    """
    dataDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    ordersData = pd.read_csv(os.path.join(dataDir, 'orders.csv'), sep=';', encoding='utf-8')
    ordersData['order_date'] = pd.to_datetime(ordersData['order_date'])
    
    # A data máxima do banco será a nossa data base de análise (como se fosse "hoje")
    maxDate = ordersData['order_date'].max()
    doisMesesAtras = maxDate - pd.DateOffset(months=2) # 2 meses de inatividade indica risco na nossa indústria de alimentos
    
    # Identificar a data da última compra de cada cliente
    ultimaCompraPorCliente = ordersData.groupby('customer_id')['order_date'].max().reset_index()
    
    # Verificamos se a data da última compra foi antes de 2 meses atrás
    ultimaCompraPorCliente['isChurn'] = ultimaCompraPorCliente['order_date'] < doisMesesAtras
    
    # Padronizando o nome das colunas
    fChurnClientes = ultimaCompraPorCliente.rename(columns={
        'customer_id': 'customerId',
        'order_date': 'lastOrderDate',
        'isChurn': 'isChurn'
    })
    
    loadToDb(fChurnClientes, 'fChurnClientes')

if __name__ == '__main__':
    print("Iniciando o processamento da fato fChurnClientes...")
    processFChurnClientes()
