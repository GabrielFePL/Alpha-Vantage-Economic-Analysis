

import os
import pandas as pd
import smtplib
from email.message import EmailMessage
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from datetime import datetime, timedelta

def fetch_and_send_email(**context):
    # Usa MsSqlHook igual ao MsSqlOperator
    hook = MsSqlHook(mssql_conn_id='mssql_default')
    sql = 'SELECT * FROM silver_agro'
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    cursor.close()
    conn.close()

    # Salva como Excel temporário
    excel_path = '/tmp/silver_agro.xlsx'
    df.to_excel(excel_path, index=False)

    # Monta o e-mail
    msg = EmailMessage()
    msg.set_content("Segue em anexo a tabela silver_agro gerada pela DAG.")
    msg['Subject'] = 'Tabela silver_agro - DAG Airflow'
    msg['From'] = 'airflowalphaprojeto@gmail.com'
    msg['To'] = 'frajacomo2@gmail.com'

    # Anexa o arquivo Excel
    with open(excel_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='silver_agro.xlsx')

    # Envia o e-mail
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('airflowalphaprojeto@gmail.com', 'hmtz jbdx uale rmmh')
        server.send_message(msg)

    # Remove o arquivo temporário
    os.remove(excel_path)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    dag_id='send_email_silver_agro_tables',
    default_args=default_args,
    description='Consulta a tabela silver_agro e envia por e-mail como Excel',
    schedule=None,
    start_date=datetime(2025, 9, 19),
    catchup=False,
    tags=['sqlserver', 'email', 'excel'],
)


send_email_task = PythonOperator(
    task_id='fetch_and_send_email',
    python_callable=fetch_and_send_email,
    dag=dag,
)
