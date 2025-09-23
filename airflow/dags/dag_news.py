from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

# O ID da conexão precisa ser idêntico ao que você criou na UI
AZURE_SQL_CONN_ID = "mssql_default"

with DAG(
    dag_id="dag_news",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["etl", "sql", "gold"],
) as dag:
    
    # Esta tarefa executa todo o código SQL diretamente da string
    process_silver_table = MsSqlOperator(
        task_id="news",
        mssql_conn_id=AZURE_SQL_CONN_ID,
        sql="""
            USE db_alpha_vantage;

            DROP TABLE IF EXISTS gold_news;

            SELECT
                calendar.date_id,
                YEAR(news.time_published) AS month,
                MONTH(news.time_published) AS year,
                news.title,
                news.time_published,
                news.url,
                news.authors,
                news.summary,
                news.source,
                news.category_within_source,
                news.source_domain,
                news.overall_sentiment_score,
                news.overall_sentiment_label,
                news.relevance_score,
                news.topic,
                news.ticker_relevance_score,
                companies.symbol as ticker,
                news.ticker as ticker_news,
                news.ticker_sentiment_score,
                news.ticker_sentiment_label
            INTO gold_news
            FROM silver_listing_companies as companies
            LEFT JOIN silver_news as news
                ON news.ticker = companies.symbol
            LEFT JOIN calendar 
                ON calendar.year = YEAR(news.time_published)
            AND calendar.month = MONTH(news.time_published)


            SELECT * FROM gold_news;
            """,
    )