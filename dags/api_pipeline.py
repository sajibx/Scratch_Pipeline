from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from scratch_pro.tasks.api_task import fetch_api_data

default_args = {
    "owner": "sajib",
    "start_date": datetime(2025, 8, 8),
    "retries": 0,
    "depends_on_past": False,
}

with DAG(
    "api_pipeline",
    default_args=default_args,
    schedule=None,
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=2),
) as dag:

    run_ts = "{{ ts_nodash }}"

    api_task = PythonOperator(
        task_id="fetch_api_data",
        python_callable=fetch_api_data,
        op_kwargs={"ts_nodash": run_ts},
        execution_timeout=timedelta(minutes=2),
    )

    api_task
