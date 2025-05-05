from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from airflow import models

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}
dag_name = "catchup_test"

with models.DAG(
    dag_name,
    default_args=default_args,
    schedule_interval="@once",
    max_active_runs=1,
    catchup=False,
    tags=["core", "dagparams"],
) as dag:

    t1 = BashOperator(task_id="catchup", bash_command="date", dag=dag)
