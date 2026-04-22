import os
import sys

# Garante que o diretório atual está no path para importar os módulos da pipeline
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.dimensao.dClientes import processDClientes
from pipeline.dimensao.dProdutos import processDProdutos
from pipeline.dimensao.dFuncionarios import processDFuncionarios

from pipeline.fato.fVendas import processFVendas
from pipeline.fato.fChurnClientes import processFChurnClientes

def runEtl():
    """
    Função principal de orquestração do pipeline ETL (Extract, Transform, Load).
    Chama os scripts de cada tabela de forma organizada.
    """
    print("Iniciando o ETL Northwind...")
    
    # Processando as Tabelas de Dimensão
    print("\n--- Processando Dimensões ---")
    processDClientes()
    processDProdutos()
    processDFuncionarios()
    
    # Processando as Tabelas Fato
    print("\n--- Processando Fatos ---")
    processFVendas()
    processFChurnClientes()
    
    print("\nETL concluído com sucesso! Os dados foram enviados para o Supabase.")

if __name__ == "__main__":
    runEtl()
