# Alpha-Vantage-Economic-Analysis
End-to-end data repository focused on US financial analysis. The pipeline collects commodity, index and enterprise data via the Alpha Vantage API. We use Docker, Apache Airflow, Azure Data Factory and SQL Server for orchestration, transformation, and storage, versioning everything on GitHub.

---

# 📘 Project Documentation – Data Pipeline with Alpha Vantage
## 1. Overview

This project aims to consume data from the Alpha Vantage API across multiple categories:

* **Commoditie:** agribusiness, fuel, minerals

* **Company Information:** company overview, listing companies

* **Economy Index**

* **State Index**

The data is extracted, stored, transformed, modeled, and delivered in multiple formats to support analysis and decision-making.

## 2. Project Architecture
### Data Flow

**1Ingestion**: Azure Data Factory consumes Alpha Vantage APIs.

**2Storage**: Raw data is stored in SQL Server.

**3Transformation**: DAGs in Apache Airflow (running in Docker) process and organize the data.

**4Modeling**: Data is structured using Data Vault methodology to ensure traceability, history, and scalability.

**5Delivery**:

* Excel tables with structured datasets

* Website for interactive data visualization

* Technical documentation (this document)

## **Simplified Diagram** 
    API[Alpha Vantage APIs] --> ADF[Azure Data Factory] 
    ADF --> SQL[SQL Server - Raw Layer] 
    SQL --> Airflow[Airflow (Docker) - Transformation] 
    Airflow --> DV[Data Vault Model] 
    DV --> Excel[Excel Data Delivery] 
    DV --> Site[Website Visualization] 

## 3. Technologies

* **Ingestion**: Azure Data Factory

* **Storage**: SQL Server

* **Transformation**: Apache Airflow (Docker)

* **Modeling**: Data Vault

* **Delivery**: Excel, Website

## 4. Data Structure
**Layers**

* **Raw Layer**: raw API data stored in SQL Server.

* **Business Vault**: business rules applied.

* **Information Mart**: curated data for final consumption (Excel and website).

**Data Vault Modeling**

* **Hubs**: core entities (e.g., Commodity, Company, Economic Index, State).

* **Links**: relationships between hubs (e.g., Commodity ↔ Price).

* **Satellites**: descriptive attributes and historical data (e.g., price over time, company descriptions, yearly indices).

## 5. Data Ingestion

* APIs configured in ADF with scheduled executions.

* Incremental storage to avoid duplication.

* Execution and error logs monitored within ADF.

## 6. Data Transformation

* Airflow DAGs organized by domain (Commodities, Companies, Economy, State).

* Standardization of formats (date, currency, indices).

* Technical keys created for Data Vault compliance.

##7. Data Delivery

**Excel**:

* Structured tables for analysis.

* One worksheet per domain (Commodities, Companies, Economy, State).

**Website**:

* Interactive dashboard for visualization.

* Filters by time period, category, and entity.

## 8. Deployment and Execution
**Requirements**

* Docker installed

* Airflow configured

* Access to SQL Server

* Alpha Vantage API keys set as environment variables

## **Startup**
    docker-compose up -d
    http://localhost:8080

## 9. Governance and Data Quality

* Data Vault methodology ensures full traceability.

* Pipelines versioned in Git.

* Automated testing in Airflow DAGs.

* Logging in both ADF and Airflow for auditing.

## 10. Deliverables

* Technical documentation (this document).

* Excel file with curated datasets.

* Website for interactive data exploration.
