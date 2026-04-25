import os
import pandas as pd
from itertools import combinations
from pipeline.utils.db import loadToDb

def processFCesta():
    """
    Função dedicada para criar e carregar a tabela fato 'fCesta' (Market Basket Analysis).
    Identificar pares de produtos que são comprados juntos no mesmo pedido e contar a frequência de co-ocorrência para viabilizar estratégias de cross-sell.
    """
    dataDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    # Carregar detalhes dos pedidos e informações dos produtos
    orderDetailsData = pd.read_csv(os.path.join(dataDir, 'order_details.csv'), sep=';', encoding='utf-8')
    productsData = pd.read_csv(os.path.join(dataDir, 'products.csv'), sep=';', encoding='utf-8')
    categoriesData = pd.read_csv(os.path.join(dataDir, 'categories.csv'), sep=';', encoding='utf-8')
    
    # Montar a dimensão de produtos com categorias para enriquecer a cesta
    productInfo = productsData.merge(categoriesData, on='category_id', how='left')
    productInfo = productInfo[['product_id', 'product_name', 'category_name']].copy()
    
    # Agrupar os produtos por pedido (quais produtos foram comprados juntos)
    productsByOrder = orderDetailsData.groupby('order_id')['product_id'].apply(list).reset_index()
    
    # Gerar todos os pares de produtos dentro de cada pedido
    pairsList = []
    for _, row in productsByOrder.iterrows():
        products = sorted(set(row['product_id']))  # Remover duplicatas e ordenar
        if len(products) >= 2:
            for productA, productB in combinations(products, 2):
                pairsList.append({'productIdA': productA, 'productIdB': productB})
    
    # Contar a frequência de cada par
    pairsDataFrame = pd.DataFrame(pairsList)
    fCesta = pairsDataFrame.groupby(['productIdA', 'productIdB']).size().reset_index(name='frequency')
    
    # Enriquecer com nomes e categorias dos produtos A e B
    fCesta = fCesta.merge(
        productInfo.rename(columns={
            'product_id': 'productIdA',
            'product_name': 'productNameA',
            'category_name': 'categoryNameA'
        }),
        on='productIdA', how='left'
    )
    fCesta = fCesta.merge(
        productInfo.rename(columns={
            'product_id': 'productIdB',
            'product_name': 'productNameB',
            'category_name': 'categoryNameB'
        }),
        on='productIdB', how='left'
    )
    
    # Ordenar por frequência decrescente para facilitar o consumo no dashboard
    fCesta = fCesta.sort_values('frequency', ascending=False).reset_index(drop=True)
    
    loadToDb(fCesta, 'fCesta')

if __name__ == '__main__':
    print("Iniciando o processamento da fato fCesta (Análise de Cesta)...")
    processFCesta()
