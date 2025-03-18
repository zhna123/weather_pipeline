# Use Apache Airflow's official image as base
FROM apache/airflow:2.7.2

# Switch to root user for installation
USER root

# Install system dependencies (Git for dbt)
RUN apt update && apt install -y git

# Switch back to airflow user
USER airflow

# Install Python packages as airflow user
RUN pip install --no-cache-dir dbt-core dbt-postgres

