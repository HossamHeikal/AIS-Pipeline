# airflow_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Importing your functions from download.py
from download import upload_to_hdfs

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 29),  # Ensure you have a start_date
    'retries': 3,
    'retry_delay': timedelta(minutes=3)
}

dag = DAG(
    'download_and_process_files',
    default_args=default_args,
    description='Download, process and upload files',
    schedule_interval=None,  # Run based on external triggers
    catchup=False
)
url = "http://web.ais.dk/aisdata/aisdk-2023-10-26.zip"
date_string = url.split('/')[-1].replace('.zip', '')
# Create the Airflow tasks

def upload_task(**kwargs):
    date = kwargs['ds']
    file_name = f"aisdk-2023-10-26.zip"
    upload_to_hdfs(file_name)

t1 = PythonOperator(
    task_id='upload_to_hdfs',
    python_callable=upload_task,
    provide_context=True,
    execution_timeout=timedelta(minutes=30),
    dag=dag
)
t2 = SparkSubmitOperator(
    application='/app/airflow/dags/convert_to_parquet.py',  # Path to your Spark application
    conn_id='spark',  # Connection ID to a Spark cluster
    task_id='submit_job',
    name='to_parquet',
    execution_timeout=timedelta(seconds=10000),  # Optional: timeout after which the job will be killed
    application_args=['{{ params.url }}'],  # Pass the URL as an argument
    dag=dag,
)
t2.params = {'url': Param('http://web.ais.dk/aisdata/aisdk-2023-10-26.zip')}
t3 = SparkSubmitOperator(
    application='/app/airflow/dags/PDA.py',  # Path to your Spark application
    conn_id='spark',  # Connection ID to a Spark cluster
    task_id='PDA',
    name='pda',
    execution_timeout=timedelta(seconds=10000),  # Optional: timeout after which the job will be killed
    application_args=['{{ params.parquetfile }}'],  # Pass the URL as an argument
    dag=dag,
)
t3.params = {'parquetfile': Param(date_string)}

t4 = SparkSubmitOperator(
    application='/app/airflow/dags/parquet_to_postgres.py',  # Update with the correct path to your script
    name='parquet_to_postgres',
    conn_id='spark',
    task_id='parquet_to_postgres_task',
    application_args=[
        "hdfs://namenode:8020/aggs/PDA/"+ date_string +".parquet",
        "postgresql+psycopg2://user:password@postgres:5432/mydatabase",
        "jdbc:postgresql://postgres:5432/mydatabase"
        "pda",
        "user",
        "password"
    ],
    dag=dag
)

# Set the task execution order
t1 >> t2 >> t3 >> t4