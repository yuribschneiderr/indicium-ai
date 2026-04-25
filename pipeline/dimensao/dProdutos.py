import os
import pandas as pd
from pipeline.utils.db import loadToDb

def processDProdutos():
    """
    Função dedicada para criar e carregar a tabela de dimensão 'dProdutos'.
    Juntar os produtos com suas respectivas categorias e padronizar as colunas.
    """
    dataDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    # Carregar os arquivos de produtos e categorias
    productsData = pd.read_csv(os.path.join(dataDir, 'products.csv'), sep=';', encoding='utf-8')
    categoriesData = pd.read_csv(os.path.join(dataDir, 'categories.csv'), sep=';', encoding='utf-8')
    
    # Juntar (merge) as duas tabelas usando a chave 'category_id'
    dProdutos = productsData.merge(categoriesData, on='category_id', how='left')
    
    # Filtrar apenas as colunas que importam para o nosso modelo
    relevantColumns = ['product_id', 'product_name', 'category_name', 'unit_price']
    dProdutos = dProdutos[relevantColumns].copy()
    
    # Padronizar o nome das colunas
    dProdutos.rename(columns={
        'product_id': 'productId',
        'product_name': 'productName',
        'category_name': 'categoryName',
        'unit_price': 'unitPrice'
    }, inplace=True)
    
    loadToDb(dProdutos, 'dProdutos')

if __name__ == '__main__':
    print("Iniciando o processamento da dimensão dProdutos...")
    processDProdutos()
