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
                calendar.month,
                calendar.year,
                calendar.date_id,
                MAX(CASE WHEN agro.name = 'Global Price of Coffee' THEN agro.value END) AS coffee_price_cents_per_pound,
                MAX(CASE WHEN agro.name = 'Global Price of Sugar' THEN agro.value END) AS sugar_price_cents_per_pound,
                MAX(CASE WHEN agro.name = 'Global Price of Wheat' THEN agro.value END) AS wheat_price_cents_per_pound,
                MAX(CASE WHEN agro.name = 'Global Price of Cotton' THEN agro.value END) AS cotton_price_dollar_per_metric_ton,
                MAX(CASE WHEN economy.name = 'Effective Federal Funds Rate' THEN economy.value END) AS federal_funds_rate_percent,
                MAX(CASE WHEN economy.name = 'Advance Retail Sales: Retail Trade' THEN economy.value END) AS retail_trade_millions_of_dollars,
                MAX(CASE WHEN economy.name = 'Consumer Price Index for all Urban Consumers' THEN economy.value END) AS [consumor_price_index_index_1982_1984_100],
                MAX(CASE WHEN fuel.name = 'Crude Oil Prices Brent' THEN fuel.value END) AS oil_brent_dollars_per_barrel,
                MAX(CASE WHEN fuel.name = 'Crude Oil Prices WTI' THEN fuel.value END) AS oil_WTI_dollars_per_barrel,
                MAX(CASE WHEN fuel.name = 'Henry Hub Natural Gas Spot Price' THEN fuel.value END) AS natural_gas_dollars_per_million_BTU,
                MAX(CASE WHEN state.name = '10-Year Treasury Constant Maturity Rate' THEN state.value END) AS treasury_percent,
                MAX(CASE WHEN state.name = 'Unemployment Rate' THEN state.value END) AS unemployment_rate_percent,
                MAX(CASE WHEN state.name = 'Real Gross Domestic Product' THEN state.value END) AS real_gross_domestic_product_billions_of_dollars,
                MAX(CASE WHEN state.name = 'Real Gross Domestic Product per Capita' THEN state.value END) AS real_gross_domestic_product_per_capita_chained_2012_dollars,
                MAX(CASE WHEN mineral.name = 'Global Price of Aluminum' THEN mineral.value END) AS Aluminium_dollar_per_metric_ton,
                MAX(CASE WHEN mineral.name = 'Global Price of Copper' THEN mineral.value END) AS Copper_dollar_per_metric_ton
            INTO gold_economic_analysis
            FROM silver_agro AS agro
            LEFT JOIN silver_economy AS economy
                ON YEAR(agro.date) = YEAR(economy.date)
            AND MONTH(agro.date) = MONTH(economy.date)
            LEFT JOIN silver_fuel AS fuel
                ON YEAR(agro.date) = YEAR(fuel.date)
            AND MONTH(agro.date) = MONTH(fuel.date)
            LEFT JOIN calendar
                ON YEAR(agro.date) = calendar.year
            AND MONTH(agro.date) = calendar.month
            LEFT JOIN silver_state_index AS state
                ON calendar.year = YEAR(state.date)
            AND calendar.month = MONTH(state.date)
            LEFT JOIN silver_mineral AS mineral
                ON calendar.year = YEAR(mineral.date)
            AND calendar.month = MONTH(mineral.date)
            GROUP BY
                calendar.date_id,
                calendar.month,
                calendar.year
            ORDER BY
                calendar.month desc;



            SELECT * FROM gold_economic_analysis
            ORDER BY year desc
                    """,
    )