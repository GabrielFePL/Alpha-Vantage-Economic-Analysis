from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook

# Nome do Conn ID que você configurou na UI do Airflow
# Certifique-se de que ele corresponda exatamente ao que você criou.
AZURE_SQL_CONN_ID = "testConnection"

with DAG(
    dag_id="azure_sql_server_dag_completa",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None, # Corrected parameter name
    tags=["azure", "sql", "exemplo"],
) as dag:
    # Esta tarefa verifica se uma tabela existe e a cria se necessário.
    # É uma boa prática para garantir que sua DAG não falhe na primeira execução.
    create_table_task = MsSqlOperator(
        task_id="create_azure_table_if_not_exists",
        mssql_conn_id=AZURE_SQL_CONN_ID,
        sql="""
            SELECT * FROM state_index_silver;
        """,
    )

    # Defina a ordem de execução do fluxo de trabalho.
    # O '>>' define a dependência: a tarefa à esquerda deve ser executada
    # antes da tarefa à direita.
    create_table_task 