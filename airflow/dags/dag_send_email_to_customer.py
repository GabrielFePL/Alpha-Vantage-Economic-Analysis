

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
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    # Busca dados da tabela gold_economic_analysis
    sql_economic = 'SELECT * FROM gold_economic_analysis'
    cursor.execute(sql_economic)
    columns_economic = [col[0] for col in cursor.description]
    data_economic = cursor.fetchall()
    df_economic = pd.DataFrame(data_economic, columns=columns_economic)
    
    # Busca dados da tabela gold_news
    sql_news = 'SELECT * FROM gold_news'
    cursor.execute(sql_news)
    columns_news = [col[0] for col in cursor.description]
    data_news = cursor.fetchall()
    df_news = pd.DataFrame(data_news, columns=columns_news)
    
    cursor.close()
    conn.close()

    # Salva como Excel temporário - Análise Econômica
    excel_path_economic = '/tmp/gold_economic_analysis.xlsx'
    df_economic.to_excel(excel_path_economic, index=False)
    
    # Salva como Excel temporário - Notícias
    excel_path_news = '/tmp/gold_news.xlsx'
    df_news.to_excel(excel_path_news, index=False)

    # Monta o e-mail
    msg = EmailMessage()
    msg.set_content(
    "Prezado(a),\n\n"
    "Conforme solicitado, encaminho em anexo as versões atualizadas das tabelas "
    "'Economic Analysis' e 'News' para este mês.\n\n"
    "Os anexos incluem:\n"
    "- gold_economic_analysis.xlsx: Análise econômica completa\n"
    "- gold_news.xlsx: Notícias e informações relacionadas\n\n"
    "Caso tenha qualquer dúvida ou precise de informações adicionais, "
    "estou à disposição.\n\n"
    "Atenciosamente,\n"
    "Equipe de Análise Econômica"
    )
    msg['Subject'] = 'Gold Economic Analysis & News - DAG Airflow'
    msg['From'] = 'airflowalphaprojeto@gmail.com'
    msg['To'] = 'frajacomo2@gmail.com'

    # Anexa o arquivo Excel - Economic Analysis
    with open(excel_path_economic, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='gold_economic_analysis.xlsx')
    
    # Anexa o arquivo Excel - News
    with open(excel_path_news, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='gold_news.xlsx')

    # Envia o e-mail
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('airflowalphaprojeto@gmail.com', 'hmtz jbdx uale rmmh')
        server.send_message(msg)

    # Remove os arquivos temporários
    os.remove(excel_path_economic)
    os.remove(excel_path_news)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    dag_id='send_email_to_customer',
    default_args=default_args,
    description='Consulta as tabelas gold_economic_analysis e gold_news e envia por e-mail como Excel',
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
