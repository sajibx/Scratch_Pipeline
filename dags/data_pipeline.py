from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scratch_pro.tasks.data_task import make_file, move_it

default_args = {
    "owner": "sajib",
    "start_date": datetime(2025, 8, 8),
    "retries": 0,
    "depends_on_past": False,
}

with DAG(
    "data_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:
    
    run_ts = "{{ ts_nodash }}"

    create_file = PythonOperator(
        task_id="create_file",
        python_callable=make_file,
        op_kwargs={"ts_nodash": run_ts},
        do_xcom_push=False,
        execution_timeout=timedelta(minutes=2),
    )

    move_file = PythonOperator(
        task_id="move_file",
        python_callable=move_it,
        op_kwargs={"ts_nodash": run_ts},
        do_xcom_push=False,
        execution_timeout=timedelta(minutes=2),
    )

    create_file >> move_file
