from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

dag = DAG(
    'delete_api_dag',
    schedule=None,
    catchup=False,
)

hello_task = BashOperator(
    task_id='delete_task',
    bash_command='echo "Hello World from Airflow!"',
    do_xcom_push = True,
    dag=dag,
)

hello_task
