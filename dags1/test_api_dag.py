from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

dag = DAG(
    'test_api_dag',
    start_date=datetime(2025, 4, 1, 3, 28, 0),
    schedule='@daily',
    is_paused_upon_creation=False,
    catchup=True
)

hello_task = BashOperator(
    task_id='test_task8',
    bash_command='echo "Hello World from Airflow!"',
    do_xcom_push = True,
    dag=dag,
)

# sleep_task = BashOperator(
#     task_id='test_task_sleep',
#     bash_command='sleep 30',
#     dag=dag,
# )

bye_task = BashOperator(
    task_id='test_task_bye',
    bash_command='echo "Bye World from Airflow!"',
    dag=dag,
)

hello_again = BashOperator(
    task_id='test_task_hello',
    bash_command='echo "Hello World from Airflow!"',
    dag=dag,
)

# hello_task
hello_task >> bye_task >> hello_again
