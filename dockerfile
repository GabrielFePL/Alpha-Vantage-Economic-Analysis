FROM apache/airflow:3.0.6

USER root
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean
USER airflow

RUN pip install pymssql methodtools && \
    pip install apache-airflow-providers-common-sql && \
    pip install --no-cache-dir "apache-airflow-providers-microsoft-mssql==3.5.0" && \
    pip install apache-airflow-providers-openlineage && \
    pip install openpyxl
 