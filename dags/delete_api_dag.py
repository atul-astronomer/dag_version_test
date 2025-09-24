from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

dag = DAG(
    'delete_api_dag',
    schedule=None,
    catchup=False,
)

hello_task = BashOperator(
    task_id='hello_task',
    bash_command='echo "Hello World Airflow!"',
    do_xcom_push = True,
    dag=dag,
)

bye_task = BashOperator(
    task_id='bye_task',
    bash_command='echo "Bye World from Airflow!"',
    do_xcom_push = True,
    dag=dag,
)

# sleep_task = BashOperator(
#     task_id='sleep_task',
#     bash_command='sleep 10',
#     do_xcom_push = True,
#     dag=dag,
# )

hello_task >> bye_task
