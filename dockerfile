FROM apache/airflow:3.0.6

USER root
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean
USER airflow
# filepath: c:\Users\julie.leal\OneDrive - Programmers Beyond IT\Desktop\Alpha_vantage\Alpha-Vantage-Economic-Analysis\dockerfile
# ...existing code...
RUN pip install pymssql methodtools && \
    pip install apache-airflow-providers-common-sql && \
    pip install --no-cache-dir "apache-airflow-providers-microsoft-mssql==3.5.0" && \
    pip install apache-airflow-providers-openlineage
# ...existing code...