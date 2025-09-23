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
    dag_id="unemployment_kpis_dag",
    default_args=default_args,
    description='Calcula KPIs de desemprego e insere no SQL Server',
    schedule=None,
    start_date=datetime(2025, 9, 18),
    catchup=False,
    tags=['kpi', 'economic', 'sqlserver'],
) as dag:

    union_query = """
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'gold_unemployment_kpis')
BEGIN
    CREATE TABLE gold_unemployment_kpis (
        Min_UnemploymentRate DECIMAL(5,2),
        Max_UnemploymentRate DECIMAL(5,2),
        Avg_UnemploymentRate DECIMAL(5,2),
        StdDev_UnemploymentRate DECIMAL(5,2),
        InsertedAt DATETIME DEFAULT GETDATE()
    );
END;

INSERT INTO gold_unemployment_kpis (Min_UnemploymentRate, Max_UnemploymentRate, Avg_UnemploymentRate, StdDev_UnemploymentRate, InsertedAt)
SELECT
    MIN(unemployment_rate_percent),
    MAX(unemployment_rate_percent),
    AVG(unemployment_rate_percent),
    STDEV(unemployment_rate_percent),
    GETDATE()
FROM gold_economic_analysis;
"""


    union_task = MsSqlOperator(
        task_id="union_task",
        mssql_conn_id="mssql_default",
        sql=union_query,
    )

    union_task
