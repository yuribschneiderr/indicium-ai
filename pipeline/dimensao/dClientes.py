import os
import pandas as pd
from pipeline.utils.db import loadToDb

def processDClientes():
    """
    Função dedicada para criar e carregar a tabela de dimensão 'dClientes'.
    Lê os dados originais de clientes e os envia ao Supabase padronizados.
    """
    # Encontra a pasta 'data' que fica dois níveis acima
    dataDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    customersFilePath = os.path.join(dataDir, 'customers.csv')
    
    # Lendo o CSV separado por ponto e vírgula
    customersData = pd.read_csv(customersFilePath, sep=';', encoding='utf-8')
    
    # Selecionando colunas relevantes para a nossa análise
    relevantColumns = ['customer_id', 'company_name', 'contact_name', 'contact_title', 'city', 'region', 'country']
    dClientes = customersData[relevantColumns].copy()
    
    # Tratando valores vazios para evitar problemas futuros no Dashboard
    dClientes.fillna('N/A', inplace=True)
    
    # Padronizando o nome das colunas
    dClientes.rename(columns={
        'customer_id': 'customerId',
        'company_name': 'companyName',
        'contact_name': 'contactName',
        'contact_title': 'contactTitle',
        'city': 'city',
        'region': 'region',
        'country': 'country'
    }, inplace=True)
    
    # Carregando no banco de dados usando a nossa função helper
    loadToDb(dClientes, 'dClientes')

if __name__ == '__main__':
    print("Iniciando o processamento da dimensão dClientes...")
    processDClientes()
