from random import randint
from textwrap import dedent
import os
from airflow import settings
from airflow.decorators import dag, task, task_group
from airflow.models import Connection
from airflow.exceptions import AirflowNotFoundException
from airflow.hooks.base_hook import BaseHook
from airflow.models.taskmixin import TaskMixin
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator


# take extra care when iterating on this file through astro
# just because you updated a plugin import doesn't mean that airflow has noticed the change
# see: https://astronomer.slack.com/archives/CGQSYG25V/p1643236770299700 for more


conn_id = "elephantsql-kashin"
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "database-1.cxmxicvi57az.us-east-2.rds.amazonaws.com")
POSTGRES_PASS = os.getenv("POSTGRES_PASS", "READ_FROM_ENV")

conn_config = Connection(
    conn_id=conn_id,
    conn_type="postgres",
    host=POSTGRES_HOST,
    login="postgres",
    password=POSTGRES_PASS,
    schema="postgres",
    port=5432,
)


@task
def create_connection():
    try:
        conn = BaseHook.get_connection(conn_id)
        print(f"Found: {conn}")
        # assuming that if it has the connection id we expect, it also has the contents that we expect
    except AirflowNotFoundException:
        session = settings.Session()
        session.add(conn_config)
        session.commit()


@task_group
def test_connection(prev_task: TaskMixin) -> TaskMixin:
    "Make sure we can talk to the DB before expecting subsequent DAGs to do so"

    test_table = "test_kashin"

    # a random number
    @task
    def pick_test_val():
        return randint(1, 99)

    test_val = pick_test_val()

    # put it in an empty database
    place_val = PostgresOperator(
        task_id="place_value",
        postgres_conn_id=conn_id,
        sql=dedent(
            f"""
                DROP TABLE IF EXISTS {test_table};
                CREATE TABLE {test_table}(num integer);
                INSERT INTO {test_table}(num) VALUES ({test_val});
                """
        ),
    )

    # get it back, is it the same?
    @task
    def check_val(expected_val):
        pg_hook = PostgresHook(postgres_conn_id=conn_id)
        num = pg_hook.get_records(sql=f"SELECT * FROM {test_table};")[0][0]
        print(f"expecting {expected_val} to be {num}")
        assert expected_val == num

    # do it in this order
    checked = check_val(test_val)
    test_val >> place_val
    prev_task >> place_val >> checked

    return checked
