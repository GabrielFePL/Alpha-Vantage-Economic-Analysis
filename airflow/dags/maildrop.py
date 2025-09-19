import smtplib
from email.message import EmailMessage
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def send_custom_email(**context):
    msg = EmailMessage()
    msg.set_content("A DAG foi executada com sucesso!")
    msg["Subject"] = "DAG Succeeded"
    msg["From"] = "airflowalphaprojeto@gmail.com"
    msg["To"] = "frajacomo2@gmail.com"

    # Use as credenciais corretas e SMTP do seu provedor
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("airflowalphaprojeto@gmail.com", "hmtz jbdx uale rmmh")
        server.send_message(msg)

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False
}

dag = DAG(
    dag_id="send_email",
    default_args=default_args,
    schedule=None,
)

bash_task = BashOperator(
    task_id="run_bash",
    bash_command='echo "DAG executed successfully!"',
    dag=dag,
)


email_task = PythonOperator(
    task_id="send_custom_email",
    python_callable=send_custom_email,
    dag=dag,
)

bash_task >> email_task
