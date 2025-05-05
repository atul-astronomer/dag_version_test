from airflow.models import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import BaseOperator

# from airflow.models.dagrun import get_task_instances
from airflow.utils.dates import days_ago

from itertools import product
from datetime import datetime, timedelta

docs = """
####Purpose
This dag tests the dag parameter 'concurrency' which sets the maximum amount of concurrent tasks in the dag.
Expected Behavior
This dag has 3 BashOperator tasks that sleep for 30 seconds each and 1 PythonOperator task.\n
The PythonOperator task compares the starts and end dates between the 3 BashOperator,\n
to ensure a BashOperator task completed separately from the 2 that were running concurrently.
"""


def get_tis(**context):
    dagrun = context["dag_run"]
    task_instances = dagrun.get_task_instances()
    # print(type(task_instances))
    three_tasks = list(filter(lambda ti: "sleep30" in ti.task_id, task_instances))
    found = None
    for one_task, other_task in product(three_tasks, three_tasks):
        if one_task.start_date > other_task.end_date:
            found = (one_task, other_task)

    if found:
        print(f"{found[0]} started after {found[1]}")
    else:
        raise Exception(
            "None of these tasks waited for the other two and the concurrency is set to 2"
        )


with DAG(
    dag_id="concurrency",
    start_date=days_ago(2),
    schedule_interval=None,
    concurrency=2,
    doc_md=docs,
    tags=["dagparams"],
) as dag:
    b0 = BashOperator(task_id="sleep30sec1", bash_command="sleep 30")
    b1 = BashOperator(task_id="sleep30sec2", bash_command="sleep 30")
    d0 = BashOperator(task_id="sleep30sec3", bash_command="sleep 30")

    py0 = PythonOperator(
        task_id="get_task_instances",
        python_callable=get_tis,
    )

[b0, b1, d0] >> py0
