from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from airflow.utils.task_group import TaskGroup


@task
def onetwothree():
    return [1, 2, 3]


@task
def consumer(value):
    print(value)


with DAG(
    dag_id="with_rename",
    start_date=datetime(1970, 1, 1),
    schedule_interval=None,
    tags=["taskmap"]
) as dag:

    with TaskGroup("tg"):
        consumer(1)  # consumer
        consumer(2)  # consumer__1
        consumer.expand(value=[1, 2, 3])
