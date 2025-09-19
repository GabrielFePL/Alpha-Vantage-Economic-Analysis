from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

# O ID da conexão precisa ser idêntico ao que você criou na UI
AZURE_SQL_CONN_ID = "mssql_default"

with DAG(
    dag_id="dag_calendar",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["etl", "sql", "silver"],
) as dag:
    
    # Esta tarefa executa todo o código SQL diretamente da string
    process_silver_table = MsSqlOperator(
        task_id="calendar_sql",
        mssql_conn_id=AZURE_SQL_CONN_ID,
        sql="""
            USE db_alpha_vantage;

            DROP TABLE IF EXISTS calendar;

            CREATE TABLE calendar
            (
                date_id INT IDENTITY(1,1) PRIMARY KEY,
                date date NOT NULL,
                month INT NOT NULL,
                year INT NOT NULL

            );

            INSERT INTO calendar (date, month, year)
            SELECT DISTINCT 
                date as data, 
                MONTH(date) AS month, 
                YEAR(date) AS year
            FROM
            (
                SELECT date FROM bronze_aluminium
                UNION ALL
                SELECT date FROM bronze_coffe
                UNION ALL
                SELECT date FROM bronze_copper
                UNION ALL
                SELECT date FROM bronze_corn
                UNION ALL
                SELECT date FROM bronze_cotton
                UNION ALL
                SELECT date FROM bronze_cpi
                UNION ALL
                SELECT date FROM bronze_federal_rates
                UNION ALL
                SELECT date FROM bronze_natural_gas
                UNION ALL
                SELECT date FROM bronze_oil_brent
                UNION ALL
                SELECT date FROM bronze_oil_wti
                UNION ALL
                SELECT date FROM bronze_real_gdp
                UNION ALL
                SELECT date FROM bronze_real_gdp_per_capita
                UNION ALL
                SELECT date FROM bronze_retail_sales
                UNION ALL
                SELECT date FROM bronze_sugar
                UNION ALL
                SELECT date FROM bronze_treasury_yield
                UNION ALL
                SELECT date FROM bronze_unemployment_rate
                UNION ALL
                SELECT date FROM bronze_wheat
            ) AS all_dates;
        """,
    )