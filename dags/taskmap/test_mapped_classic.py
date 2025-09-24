from airflow.sdk import DAG
from airflow.decorators import task
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta


@task
def make_arg_lists():
    return [[1], [2], [{"a": "b"}], ["hello"]]


def consumer(value):
    print(value)


with DAG(
    dag_id="test_mapped_classic",
    start_date=datetime(1970, 1, 1),
    schedule=None,
    tags=["taskmap"]
) as dag:
    PythonOperator.partial(task_id="consumer1", python_callable=consumer).expand(
        op_args=make_arg_lists()
    )
