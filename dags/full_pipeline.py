from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import logging

DATA_ROOT = Path("/Users/ashiqurrahman/DE_Projects/airflow29_home/data")
TMP = DATA_ROOT / "tmp"
DEST = DATA_ROOT / "dest"
log = logging.getLogger(__name__)

# Generate timestamp ONCE when DAG is triggered
RUN_TS = "{{ ts_nodash }}"

def make_file(ts_nodash):
    TMP.mkdir(parents=True, exist_ok=True)
    p = TMP / f"my_file_{ts_nodash}.txt"
    p.write_text("This is my file, created by python\n")
    log.info("Created %s", p)

def move_it(ts_nodash):
    src = TMP / f"my_file_{ts_nodash}.txt"
    DEST.mkdir(parents=True, exist_ok=True)
    dst = DEST / f"my_file_{ts_nodash}.txt"
    shutil.move(str(src), str(dst))
    log.info("Moved %s -> %s", src, dst)

default_args = {
    "owner": "sajib",
    "start_date": datetime(2025, 8, 8),
    "retries": 0,
    "depends_on_past": False,
}

with DAG(
    "full_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:
    run_ts = "{{ ts_nodash }}"

    create_file = PythonOperator(
        task_id="create_file",
        python_callable=make_file,
        op_kwargs={"ts_nodash": run_ts}
    )
    move_file = PythonOperator(
        task_id="move_file",
        python_callable=move_it,
        op_kwargs={"ts_nodash": run_ts}
    )

    create_file >> move_file
