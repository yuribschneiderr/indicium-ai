# Northwind Traders Analytics — Relatório Executivo

Este repositório contém uma solução completa de **Engenharia de Dados e Business Intelligence** projetada para transformar dados operacionais da Northwind Traders em insights estratégicos.

---

## Visão Geral do Projeto

O objetivo central é fornecer ao corpo executivo uma visão unificada sobre **Faturamento, Comportamento de Compra (Cross-Sell) e Fidelidade de Clientes (Churn)**. A solução abrange desde a extração de dados brutos até a visualização em um dashboard interativo projetado para suporte à decisão.

### Diferenciais Técnicos
- **Pipeline ETL Escalável**: Processamento de dados transacionais com tratamento de lógica de negócios (descontos, datas de entrega e regionalização).
- **Banco de Dados Cloud**: Integração nativa com **Supabase (PostgreSQL)** via camada transacional e analítica.
- **Visualização Executiva**: Dashboard construído em **Streamlit** com design limpo (pastel azul), rótulos de dados nativos e layout otimizado para **exportação em PDF**.
- **Infraestrutura como Código**: Ambiente totalmente isolado e reprodutível via **Docker & Docker Compose**.

---

## Inteligência de Negócio Implementada

### 1. Monitoramento Granular de Churn
Diferente de modelos binários, implemento uma régua de fidelidade em 3 níveis:
- **Ativo**: < 45 dias de inatividade.
- **Em Risco**: 45–60 dias (Janela crítica para intervenção).
- **Churn**: > 60 dias (Inatividade confirmada).

### 2. Market Basket Analysis (Análise de Cesta)
Algoritmo de associação que identifica quais produtos e categorias são comprados juntos com maior frequência. Esta análise é a base para o plano de ação de **Cross-Sell** e aumento do **Ticket Médio**.

### 3. Expansão Regional
Mapeamento geográfico de performance para identificar mercados com alta demanda, mas baixo ticket médio, orientando a expansão de centros de distribuição.

---

## Como Executar o Projeto

1.  **Clone o repositório** e garanta que possui o **Docker** instalado.
2.  Configure suas credenciais do banco no arquivo `.env` (exemplo: `DATABASE_URL=postgresql://user:pass@host:port/db`).
3.  Execute o comando:
    ```bash
    docker-compose up --build -d
    ```
4.  Acesse o dashboard em: `http://localhost:8501`.

---

## Dashboard Publicado

O relatório executivo está disponível online via Streamlit Cloud:

**[Acessar Dashboard via Streamlit Cloud](https://indicium-ai-49xwsufu8fexdnfxzczuyh.streamlit.app/)**

---

## Plano de Ação Estratégico
O dashboard inclui um módulo fixo de recomendações que utiliza os dados processados para sugerir:
- Criação de combos promocionais baseados em co-ocorrência.
- Programas de reativação proativa para clientes na zona de risco (45-60 dias).
- Estratégias preventivas de sazonalidade.

---
*Este projeto foi desenvolvido como um desafio técnico de Data Engineering & Analytics.*
