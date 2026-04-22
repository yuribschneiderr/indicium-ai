# 📊 Relatório Executivo e Documentação: Northwind Analytics

> [!NOTE]
> **Data:** Abril de 2026
> **Para:** Tony Stark, CEO da Northwind Traders
> **Assunto:** Análise de Faturamento, Ticket Médio e Churn (Janela de 2 Meses)

## 📌 Contexto Estratégico

Este projeto foi construído para fornecer uma visão integrada e ágil dos dados fragmentados da Northwind Traders. Através de um pipeline **ETL** (Extract, Transform, Load) construído em **Python**, os dados de planilhas locais foram processados e transformados em um **Star Schema**, centralizando-os em um banco de dados relacional (Supabase/PostgreSQL).

A partir deste repositório centralizado, construímos um painel interativo (App Streamlit) para monitorar nossos principais indicadores de performance (KPIs).

## 🚀 Arquitetura Implementada

- **Pipeline (ETL):** Módulos Python em `pipeline/dimensao/` e `pipeline/fato/` extraem, limpam e relacionam dados de 14 planilhas.
- **Banco de Dados:** Utilização do PostgreSQL via **Supabase** para uma camada de armazenamento robusta e acessível.
- **Visualização (BI):** Dashboard interativo em **Streamlit**, projetado para permitir análises aprofundadas.
- **Ambiente Isolado:** Configuração completa com **Docker** (`docker-compose`), garantindo que qualquer analista da Northwind possa rodar a aplicação em segundos com o comando `docker-compose up`.

---

## 📈 Principais Indicadores Analisados (KPIs)

O Dashboard apresenta os seguintes indicadores-chave (com dados projetados até o último ano registrado, 1998):

### 1. Faturamento e Pedidos
- **Faturamento Total:** Calculado pelo preço dos itens, quantidade e descontos aplicados.
- **Total de Pedidos Realizados.**
- **Ticket Médio:** Permite identificar sazonalidades. Recomenda-se realizar campanhas de *cross-sell* oferecendo produtos correlatos (ex: oferecer queijos e cervejas na compra de vinhos) para elevar este número.

### 2. Taxa de Churn (Inatividade)
- **Definição de Churn (2 meses):** Clientes que não realizaram pedidos nos últimos 60 dias (em relação à data máxima do banco de dados).
- Como somos uma empresa focada no ramo de alimentos e bebidas, **um cliente que não compra há mais de 2 meses é considerado um cliente em risco (churn).**
- O painel exibe um gráfico de proporção dos clientes ativos vs. clientes perdidos na janela estipulada.

### 3. Top 10 Produtos por Receita
- A visualização identifica exatamente onde se encontra o nosso maior *Market Share*. O foco promocional (Upselling) deve ser mantido nestes "Carros-Chefe".

---

## 💡 Próximos Passos e Recomendações (Ações de Negócio)

> [!TIP]
> **Ações sugeridas baseadas na análise de dados:**

1. **Aumentar o Ticket Médio:**
   - Criar pacotes (Combos) com base nos Top 10 produtos de maior faturamento.
   - Implementar estratégias de desconto por volume ("Leve 3, Pague 2") em produtos de giro médio.

2. **Reduzir o Churn:**
   - Como o ciclo de vida dos nossos produtos é curto (2 meses para Churn), devemos implementar um alerta automático para clientes que não compram há **45 dias**.
   - Oferecer cupons exclusivos ou amostras de lançamentos (ex: Frete Grátis) para clientes que estão se aproximando dos 60 dias de inatividade.

---

## 🛠 Como Rodar este Projeto (Instruções Técnicas)

Se desejar executar a aplicação na sua própria máquina, o repositório contém tudo pronto para uso.

1. **Pré-requisito:** Instalar Docker e Docker Compose.
2. **Execução:**
   Abra o terminal na pasta do projeto e execute:
   ```bash
   docker-compose up --build
   ```
3. O pipeline de **ETL** (`northwind-etl`) irá rodar automaticamente e fazer o upload/atualização no Supabase.
4. O painel do **Streamlit** (`northwind-app`) subirá e ficará acessível no navegador pelo endereço:
   - `http://localhost:8501`

*(Para exportar este painel em PDF, basta abrir o Streamlit no Google Chrome, clicar em "Imprimir" (`Ctrl+P`) e selecionar "Salvar como PDF").*
