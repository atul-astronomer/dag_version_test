from random import randint
from textwrap import dedent

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


conn_id = "kubernetes_default"

conn_config = Connection(
    conn_id=conn_id,
    conn_type="Kubernetes Cluster Connection",
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

