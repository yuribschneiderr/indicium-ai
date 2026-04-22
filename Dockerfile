FROM python:3.11-slim

WORKDIR /app

# Instalar dependências necessárias para psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos da aplicação
COPY ./app ./app
COPY ./pipeline ./pipeline
COPY runEtl.py .

# Porta do Streamlit
EXPOSE 8501

# O comando padrão iniciará o dashboard
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
