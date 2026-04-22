import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Pegamos a URL de conexão do arquivo .env
dbUrl = os.environ.get("DATABASE_URL")
if not dbUrl:
    raise ValueError("A variável de ambiente DATABASE_URL não foi encontrada. Verifique seu arquivo .env")

def getEngine():
    """
    Cria e retorna a engine (motor) de conexão com o banco de dados Supabase.
    Essa engine é a responsável por traduzir nossas intenções do Pandas para o Postgres.
    """
    return create_engine(dbUrl)

def loadToDb(dataFrame: pd.DataFrame, tableName: str, schemaName: str = 'public'):
    """
    Carrega (Load) um DataFrame para o banco de dados.
    Caso a tabela já exista, ela será substituída (replace).
    
    Parâmetros:
    - dataFrame: A tabela de dados em memória que queremos salvar.
    - tableName: O nome da tabela que ficará no banco.
    - schemaName: O schema do banco, por padrão 'public'.
    """
    dbEngine = getEngine()
    # Usamos if_exists='replace' para garantir que os dados sejam atualizados a cada execução do pipeline
    dataFrame.to_sql(name=tableName, con=dbEngine, schema=schemaName, if_exists='replace', index=False)
    print(f"A tabela '{tableName}' foi carregada com sucesso! Um total de {len(dataFrame)} linhas foram inseridas.")
