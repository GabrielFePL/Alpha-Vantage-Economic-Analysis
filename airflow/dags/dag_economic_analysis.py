from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

# O ID da conexão precisa ser idêntico ao que você criou na UI
AZURE_SQL_CONN_ID = "mssql_default"

with DAG(
    dag_id="dag_economic_analysis",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["etl", "sql", "gold"],
) as dag:
    
    # Esta tarefa executa todo o código SQL diretamente da string
    process_silver_table = MsSqlOperator(
        task_id="economic_analysis",
        mssql_conn_id=AZURE_SQL_CONN_ID,
        sql="""
            USE db_alpha_vantage;

            DROP TABLE gold_economic_analysis

            SELECT
                calendar.date,
                calendar.date_id,
                MAX(CASE WHEN agro.name = 'Global Price of Coffee' THEN agro.value ELSE NULL END) AS coffee_price,
                MAX(CASE WHEN agro.name = 'Global Price of Sugar' THEN agro.value ELSE NULL END) AS sugar_price,
                MAX(CASE WHEN agro.name = 'Global Price of Wheat' THEN agro.value ELSE NULL END) AS wheat_price,
                MAX(CASE WHEN agro.name = 'Global Price of Cotton' THEN agro.value ELSE NULL END) AS cotton_price,
                MAX(CASE WHEN economy.name = 'Effective Federal Funds Rate' THEN economy.value ELSE NULL END) AS federal_funds_rate,
                MAX(CASE WHEN economy.name = 'Advance Retail Sales: Retail Trade' THEN economy.value ELSE NULL END) AS retail_trade,
                MAX(CASE WHEN economy.name = 'Consumer Price Index for all Urban Consumers' THEN economy.value ELSE NULL END) AS consumor_price_index,
                MAX(CASE WHEN fuel.name = 'Crude Oil Prices Brent' THEN fuel.value ELSE NULL END) AS oil_brent,
                MAX(CASE WHEN fuel.name = 'Crude Oil Prices WTI' THEN fuel.value ELSE NULL END) AS oil_WTI,
                MAX(CASE WHEN fuel.name = 'Henry Hub Natural Gas Spot Price' THEN fuel.value ELSE NULL END) AS natural_gas,
                MAX(CASE WHEN state.name = '10-Year Treasury Constant Maturity Rate' THEN state.value ELSE NULL END) AS treasury,
                MAX(CASE WHEN state.name = 'Unemployment Rate' THEN state.value ELSE NULL END) AS unemployment_rate,
                LAST_VALUE(MAX(CASE WHEN state.name = 'Real Gross Domestic Product' THEN state.value ELSE NULL END)) IGNORE NULLS OVER (ORDER BY calendar.date) AS real_gross_domestic_product,
                LAST_VALUE(MAX(CASE WHEN state.name = 'Real Gross Domestic Product per Capita' THEN state.value ELSE NULL END)) IGNORE NULLS OVER (ORDER BY calendar.date) AS real_gross_domestic_product_per_capita
            INTO gold_economic_analysis
            FROM
                silver_agro as agro
            LEFT JOIN silver_economy AS economy
            ON agro.date = economy.date
            LEFT JOIN silver_fuel as fuel
            ON agro.date = fuel.date
            LEFT JOIN calendar
            ON calendar.date = agro.date
            LEFT JOIN silver_state_index as state
            ON calendar.date = state.date
            GROUP BY
                calendar.date,
                calendar.date_id
            ORDER BY
                calendar.date DESC;


            SELECT * FROM gold_economic_analysis
            ORDER BY date desc
        """,
    )