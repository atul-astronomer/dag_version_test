from random import randint
from textwrap import dedent

from airflow import settings
from airflow.decorators import dag, task, task_group
from airflow.models import Connection
from airflow.exceptions import AirflowNotFoundException
from airflow.hooks.base_hook import BaseHook
from airflow.models.taskmixin import TaskMixin
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

# take extra care when iterating on this file through astro
# just because you updated a plugin import doesn't mean that airflow has noticed the change
# see: https://astronomer.slack.com/archives/CGQSYG25V/p1643236770299700 for more

conn_id = "sqlite-pocketsand"
db_file_path = "/sqlite3/pocketsand.db"
table_name = "personage"
dockerfile_fragment = dedent(
    f"""
    apt update && apt install sqlite3
    mkdir /sqlite3
    sqlite3 {db_file_path} "CREATE TABLE IF NOT EXISTS {table_name}(name varchar, age integer);"
    sqlite3 {db_file_path} "INSERT INTO {table_name}(name, age) VALUES ('Chi', 23), ('Fred', 25);"
    """
)

conn_config = Connection(
    conn_id=conn_id,
    conn_type="sqlite",
    host=db_file_path,
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


def test_connection(prev_task: TaskMixin) -> TaskMixin:
    "Make sure we can talk to the DB before leaving it to subsequent DAGs to do so"

    # can we read from it?
    @task
    def check_connection():
        pg_hook = SqliteHook(sqlite_conn_id=conn_id)
        result = pg_hook.get_records(sql=f"SELECT * FROM {table_name};")
        print(result)
        assert len(result) == 2
        for row in result:
            for val in row:
                print(f"got {val}")
                assert val in ["Chi", 23, "Fred", 25]

    checked = check_connection()
    prev_task >> checked

    return checked
