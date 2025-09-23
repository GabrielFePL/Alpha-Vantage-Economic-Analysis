from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_silver_transformation_news_table",
    default_args=default_args,
    description="Trata tabela de notícias no SQL Server",
    schedule=None,
    start_date=datetime(2025, 9, 18),
    catchup=False,
    tags=["sqlserver", "union"],
) as dag:

    union_query = """
    SELECT 
        [items],
        [title],
        [url],
        CAST(
            STUFF(STUFF(LEFT([time_published], 8), 5, 0, '-')
                , 8, 0, '-') + ' ' +
            STUFF(STUFF(RIGHT([time_published], 6), 3, 0, ':')
                , 6, 0, ':')
        AS DATE) AS [time_published],
        [authors],
        [summary],
        [banner_image],
        [source],
        [category_within_source],
        [source_domain],
        [overall_sentiment_score],
        [overall_sentiment_label],
        [relevance_score],
        [topic],
        [ticker_relevance_score],
        [ticker],
        [ticker_sentiment_score],
        [ticker_sentiment_label]
    INTO silver_news
    FROM [dbo].[bronze_news];
    """

    union_task = MsSqlOperator(
        task_id="union_task",
        mssql_conn_id="mssql_default",  # conexão criada no Airflow UI
        sql=union_query,
    )

    union_task
