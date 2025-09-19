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
    dag_id="dag_union_tables_agro",
    default_args=default_args,
    description="Faz UNION de 3 tabelas no SQL Server",
    schedule=None,
    start_date=datetime(2025, 9, 18),
    catchup=False,
    tags=["sqlserver", "union"],
) as dag:

    union_query = """
    SELECT name, interval, unit, date, value
    INTO silver_agro FROM
    (
        SELECT name, interval, unit, date, value FROM bronze_coffe
        UNION
        SELECT name, interval, unit, date, value FROM bronze_wheat
        UNION
        SELECT name, interval, unit, date, value FROM bronze_cotton
        UNION
        SELECT name, interval, unit, date, value FROM bronze_corn
        UNION
        SELECT name, interval, unit, date, value FROM bronze_sugar
    ) AS silver_agro;
    """

    union_task = MsSqlOperator(
        task_id="union_task",
        mssql_conn_id="mssql_default",  # conexão criada no Airflow UI
        sql=union_query,
    )

    union_task
