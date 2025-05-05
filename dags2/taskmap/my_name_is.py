from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from airflow.models import TaskInstance


@task
def mynameis(arg, **context):

    ti: TaskInstance = context["ti"]
    print(ti.task_id)
    print(arg)


with DAG(
    dag_id="my_name_is",
    start_date=datetime(1970, 1, 1),
    schedule_interval=None,
    tags=["taskmap"]
) as dag:
    mynameis.expand(arg=["slim", "shady"])
