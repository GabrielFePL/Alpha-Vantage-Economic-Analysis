from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

# O ID da conexão precisa ser idêntico ao que você criou na UI
AZURE_SQL_CONN_ID = "testConnection"

with DAG(
    dag_id="etl_silver_state_index",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["etl", "sql", "silver"],
) as dag:
    
    # Esta tarefa executa todo o código SQL diretamente da string
    process_silver_table = MsSqlOperator(
        task_id="silver_state_index",
        mssql_conn_id=AZURE_SQL_CONN_ID,
        sql="""
            USE db_alpha_vantage;

            DROP TABLE IF EXISTS silver_state_index;

            SELECT name, interval, unit, date, value
            INTO silver_state_index FROM
            (
                SELECT name, interval, unit, date, value FROM bronze_real_gdp
                UNION ALL
                SELECT name, interval, unit, date, value FROM bronze_real_gdp_per_capita
                UNION ALL
                SELECT name, interval, unit, date, value FROM bronze_treasury_yield
                UNION ALL 
                SELECT name, interval, unit, date, value FROM bronze_unemployment_rate
            ) AS state_index_silver;
            
            SELECT * FROM silver_state_index;
        """,
    )