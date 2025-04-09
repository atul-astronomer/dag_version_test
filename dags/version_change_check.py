from datetime import datetime

from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG

from providers.standard.src.airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id="version_change", schedule=None, start_date=datetime(1970, 1, 1), catchup=True, tags=["taskmap"]
) as dag:

    task1 = EmptyOperator(task_id='task1')
    task2 = BashOperator(task_id='task2', bash_command="sleep 20")
    task3 = EmptyOperator(task_id='task3')

task1 >> task2 >> task3
