import json
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task


@dag(
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=['shrd-task-vol'])
def example_dag_with_shared_task_volume():
    """
    ### Basic Dag
    This is a basic dag with task using shared data volume to communicate
    """

    @task()
    def write():
        """
        #### Write task
        A simple "write" task to write data to /usr/local/airflow/data/test.txt file, wherein
        /usr/local/airflow/data is shared volume between tasks.
        """
        data_string = "test data string"

        file = open('/usr/local/airflow/data/test.txt', 'w+')
        file.write(data_string)
        file.close()

    @task()
    def read():
        """
        #### Read task
        A simple "read" task which reads file at /usr/local/airflow/data/test.txt
        and compare the file content to expected string.
        """
        total_order_value = 0

        file = open('/usr/local/airflow/data/test.txt', 'r')
        file_data = file.read()
        file.close()
        assert file_data == "test data string"

    write = write()
    read = read()

example_dag_with_shared_task_volume = example_dag_with_shared_task_volume()
