# from airflow.providers.standard.operators.bash import BashOperator
from pendulum import today

from airflow import models
from providers.standard.src.airflow.providers.standard.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "start_date": today('UTC').add(days=-1),
}
dag_name = "catchup_test"

with models.DAG(
    dag_name,
    default_args=default_args,
    schedule="@once",
    max_active_runs=1,
    catchup=False,
    tags=["core", "dagparams"],
) as dag:

    t1 = BashOperator(task_id="catchup", bash_command="date", dag=dag)
