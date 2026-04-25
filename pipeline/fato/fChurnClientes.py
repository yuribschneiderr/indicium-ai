import os
import pandas as pd
from pipeline.utils.db import loadToDb

def processFChurnClientes():
    """
    Função dedicada para criar e carregar a tabela fato (ou tabela derivada) 'fChurnClientes'.
    Aqui verificar a última compra do cliente e calcular se ele deu Churn
    baseado na regra de 2 meses sem comprar (60 dias).
    """
    dataDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    ordersData = pd.read_csv(os.path.join(dataDir, 'orders.csv'), sep=';', encoding='utf-8')
    ordersData['order_date'] = pd.to_datetime(ordersData['order_date'])
    
    # A data máxima do banco será a nossa data base de análise (como se fosse "hoje")
    maxDate = ordersData['order_date'].max()
    
    # Identificar a data da última compra de cada cliente
    ultimaCompraPorCliente = ordersData.groupby('customer_id')['order_date'].max().reset_index()
    
    # Calcular quantos dias se passaram desde a última compra de cada cliente
    ultimaCompraPorCliente['daysSinceLastOrder'] = (maxDate - ultimaCompraPorCliente['order_date']).dt.days
    
    # Classificação em 3 níveis:
    # - "Churn": sem comprar há mais de 60 dias (2 meses)
    # - "Em Risco": sem comprar há mais de 45 dias, mas menos de 60
    # - "Ativo": comprou nos últimos 45 dias
    def classifyChurnStatus(days):
        if days > 60:
            return 'Churn'
        elif days > 45:
            return 'Em Risco'
        else:
            return 'Ativo'
    
    ultimaCompraPorCliente['churnStatus'] = ultimaCompraPorCliente['daysSinceLastOrder'].apply(classifyChurnStatus)
    
    # Manter também o flag binário para compatibilidade
    ultimaCompraPorCliente['isChurn'] = ultimaCompraPorCliente['daysSinceLastOrder'] > 60
    
    # Padronizar o nome das colunas
    fChurnClientes = ultimaCompraPorCliente.rename(columns={
        'customer_id': 'customerId',
        'order_date': 'lastOrderDate',
    })
    
    loadToDb(fChurnClientes, 'fChurnClientes')

if __name__ == '__main__':
    print("Iniciando o processamento da fato fChurnClientes...")
    processFChurnClientes()
