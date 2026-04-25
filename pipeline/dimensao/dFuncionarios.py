import os
import pandas as pd
from pipeline.utils.db import loadToDb

def processDFuncionarios():
    """
    Função dedicada para criar e carregar a tabela de dimensão 'dFuncionarios'.
    Aqui juntar nome e sobrenome do funcionário para facilitar a análise e padronizar o nome das colunas.
    """
    dataDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    employeesData = pd.read_csv(os.path.join(dataDir, 'employees.csv'), sep=';', encoding='utf-8')
    
    # Criar um nome completo mais amigável
    employeesData['full_name'] = employeesData['first_name'] + ' ' + employeesData['last_name']
    
    # Filtrar as colunas que nos interessam
    relevantColumns = ['employee_id', 'full_name', 'title', 'city', 'country']
    dFuncionarios = employeesData[relevantColumns].copy()
    
    # Remover vazios e colocar N/A
    dFuncionarios.fillna('N/A', inplace=True)
    
    # Padronizar o nome das colunas
    dFuncionarios.rename(columns={
        'employee_id': 'employeeId',
        'full_name': 'fullName',
        'title': 'title',
        'city': 'city',
        'country': 'country'
    }, inplace=True)
    
    loadToDb(dFuncionarios, 'dFuncionarios')

if __name__ == '__main__':
    print("Iniciando o processamento da dimensão dFuncionarios...")
    processDFuncionarios()
