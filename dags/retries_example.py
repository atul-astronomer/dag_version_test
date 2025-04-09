from datetime import datetime, timedelta

from airflow.sdk import DAG
from providers.standard.src.airflow.providers.standard.operators.python import PythonOperator


# Python function to simulate the task with division by zero
def division_by_zero():
    num = 10
    denom = 0  # This will trigger a ZeroDivisionError
    result = num / denom  # Division by zero
    return result

# Define the DAG
default_args = {
    'owner': 'airflow',
    'retries': 3,  # Retry the task 3 times
    'retry_delay': timedelta(seconds=5),  # Delay between retries
}

dag = DAG(
    'division_by_zero_example',
    default_args=default_args,
    description='An example DAG where task fails due to division by zero',
    schedule=None,  # No automatic scheduling, run manually
    start_date=datetime(2025, 2, 10),
    catchup=False,
)

# Define the task that will fail
task1 = PythonOperator(
    task_id='task_with_failure',
    python_callable=division_by_zero,
    # provide_context=True,  # Pass context to Python function if needed
    dag=dag,
)

task1
