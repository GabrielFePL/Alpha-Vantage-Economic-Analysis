from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.operators.python import PythonOperator

# O ID da conexão precisa ser idêntico ao que você criou na UI
AZURE_SQL_CONN_ID = "testConnection"

# Função Python que irá executar a consulta e imprimir o resultado
def get_query_results_and_print():
    # Instancia o hook para se conectar ao SQL Server
    mssql_hook = MsSqlHook(mssql_conn_id=AZURE_SQL_CONN_ID)
    
    # Executa a consulta
    query = "SELECT * FROM state_index_silver;"
    result = mssql_hook.get_records(query)
    
    # Imprime o resultado. Isso aparecerá nos logs da tarefa do Airflow.
    print("Início do Output da Query:")
    for row in result:
        print(row)
    print("Fim do Output da Query.")

with DAG(
    dag_id="azure_sql_server_dag_completa_com_output",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["azure", "sql", "exemplo"],
) as dag:
    get_output_task = PythonOperator(
        task_id="get_query_output",
        python_callable=get_query_results_and_print,
    )