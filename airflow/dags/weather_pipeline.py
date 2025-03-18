from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
# Allows Airflow to import scripts from the scripts/ folder inside the container
# Necessary because Airflow runs inside Docker, and the scripts/ folder is not a standard Python path
sys.path.append("/opt/weather_pipeline/scripts")  

from db_utils import create_staging_table
from load_weather_data import load_all_csvs_to_postgres

# DAG configuration - Default arguments
default_args = {
    'owner': 'airflow',   # The owner of the DAG
    'depends_on_past': False,  # DAG runs independently of past runs
    'start_date': datetime(2024, 3, 1),  # When the DAG should start running
    'retries': 0
    # 'retries': 1,  # If a task fails, retry once
    # 'retry_delay': timedelta(minutes=5),  # Wait 5 minutes before retrying
}

# Define the DAG
with DAG('weather_pipeline',   # DAG name
         default_args=default_args,
         schedule_interval='@daily',  # Run once a day
         catchup=False) as dag:  # does not backfill missing historical runs
    
    # ensure table exists 
    create_table = PythonOperator(
        task_id="create_staging_table",
        python_callable=create_staging_table
    )

    # Task 1: Load raw csv data into Postgres
    load_data = PythonOperator(
        task_id="load_data",
        python_callable=load_all_csvs_to_postgres
    )

    # Task 2: Run dbt models
    run_dbt_models = BashOperator(
        task_id='run_dbt_models',
        # Look for profiles.yml inside /opt/weather_pipeline/dbt instead of the default location.
        # Tell dbt where to find dbt_project.yml
        bash_command='dbt run --profiles-dir /opt/weather_pipeline/dbt --project-dir /opt/weather_pipeline/dbt'
    )

    # Task 3: Validate Data
    def validate_data():
        import psycopg2
        conn = psycopg2.connect(
            host="postgres",
            database="weather",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM int_weather_trends")
        count = cur.fetchone()[0]
        if count < 1:
            raise ValueError("Data validation failed: No records in table.")
        conn.close()

    # Uses a PythonOperator to execute custom Python code
    validate = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data
    )

    # Task 4: Archive old data (optional)
    # Runs a script to move older data from raw tables to an archive.
    # archive_data = BashOperator(
    #     task_id='archive_data',
    #     bash_command='python /opt/weather_pipeline/scripts/archive_old_data.py'
    # )

    # Define dependencies
    create_table >> load_data >> run_dbt_models >> validate
