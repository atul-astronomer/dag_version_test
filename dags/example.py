from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
# from airflow.operators.bash import BashOperator

dag = DAG(
    'hello_world_dag',
    schedule=None,
    catchup=False,
)

hello_task = BashOperator(
    task_id='say_hello',
    bash_command='echo "Hello World from Airflow!"',
    do_xcom_push = True,
    dag=dag,
)

hello_task
