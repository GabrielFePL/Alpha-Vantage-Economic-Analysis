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
    dag_id="dag_silver_transform_listing_companies_table",
    default_args=default_args,
    description="Transforma CSV nvarchar em tabela estruturada silver_listing_companies",
    schedule=None,
    start_date=datetime(2025, 9, 18),
    catchup=False,
    tags=["sqlserver", "csv", "bronze", "silver"],
) as dag:

    transform_query = """
    -- Remove e recria a tabela destino
    IF OBJECT_ID('silver_listing_companies') IS NOT NULL
        DROP TABLE silver_listing_companies;

    CREATE TABLE silver_listing_companies (
        symbol NVARCHAR(50),
        name NVARCHAR(200),
        exchange NVARCHAR(50),
        assetType NVARCHAR(50),
        ipoDate NVARCHAR(50),
        delistingDate NVARCHAR(50),
        status NVARCHAR(50)
    );

    DECLARE @csv NVARCHAR(MAX);
    SELECT @csv = body FROM bronze_listing_companies;

    ;WITH lines AS (
        SELECT value AS line,
               ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn
        FROM STRING_SPLIT(@csv, CHAR(10))
        WHERE LTRIM(RTRIM(value)) <> ''
    ),
    data_lines AS (
        SELECT line
        FROM lines
        WHERE rn > 1  -- ignora o cabeçalho
    ),
    cols AS (
        SELECT dl.line,
               ROW_NUMBER() OVER (PARTITION BY dl.line ORDER BY (SELECT NULL)) AS col_num,
               LTRIM(RTRIM(value)) AS col_value
        FROM data_lines dl
        CROSS APPLY STRING_SPLIT(dl.line, ',')
    )
    INSERT INTO silver_listing_companies (symbol, name, exchange, assetType, ipoDate, delistingDate, status)
    SELECT
        MAX(CASE WHEN col_num = 1 THEN col_value END) AS symbol,
        MAX(CASE WHEN col_num = 2 THEN col_value END) AS name,
        MAX(CASE WHEN col_num = 3 THEN col_value END) AS exchange,
        MAX(CASE WHEN col_num = 4 THEN col_value END) AS assetType,
        MAX(CASE WHEN col_num = 5 THEN col_value END) AS ipoDate,
        MAX(CASE WHEN col_num = 6 THEN col_value END) AS delistingDate,
        MAX(CASE WHEN col_num = 7 THEN col_value END) AS status
    FROM cols
    GROUP BY line;
    """

    transform_task = MsSqlOperator(
        task_id="transform_listing_companies",
        mssql_conn_id="mssql_default",
        sql=transform_query,
    )

    transform_task
