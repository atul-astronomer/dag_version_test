from datetime import datetime

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk.exceptions import AirflowRuntimeError

from airflow.hooks.base import BaseHook
from airflow.sdk import DAG
from airflow.models import Connection
from dags.plugins import api_utility
from dags.plugins.api_utility import delete_connection

docs = """
####Purpose
The purpose of this dag is to test that URI's are successfully generated when using the Connection.get_uri() method.\n
It achieves this test by making an assertion that the URI is the in the correct format.
####Expected Behavior
This dag has 2 tasks in it both of which are expected to succeed.\n
The first task sets up a fake connection for testing purposes.\n
The second task makes an assertion that the value of the URI is the in the correct format for the data that was added with the Connection class.
"""

dag_name = "test_uri_generation"


def add_conn():
    try:
        found = BaseHook().get_connection(f"{dag_name}_connection")
        print("The connection has been made previously.")
    except Exception:
        found = None
        request_body = {
            "connection_id": f"{dag_name}_connection",
            "conn_type": "conn_type_string",
            "host": "dns_name.dns",
            "login": "username",
            "schema": "database_scheme",
            "port": 33302,
            "password": "password"
        }
        response = api_utility.create_connection(request_body)
        assert response.json()['connection_id'] == f"{dag_name}_connection"


def check_uri_gen():
    try:
        c = Connection()
        conn = c.get_connection_from_secrets(f"{dag_name}_connection")
        uri = conn.get_uri()
        print("An assert is being made below that the uri is of type string")
        assert isinstance(uri, str)
        print(f"The uri is: {uri}")
        print("An assert is being made below that the get_uri() function of the Connection class is working correctly correctly")
        assert uri == "conn-type-string://username:password@dns_name.dns:33302/database_scheme"
    except AirflowRuntimeError:
        print("There is no connection to pull data from.")
    finally:
        #clean up the connection by deleting it
        delete_response = delete_connection(conn.conn_id)
        assert delete_response.status_code == 204

with DAG(
    dag_id=dag_name,
    start_date=datetime(2021, 1, 1),
    schedule=None,
    doc_md=docs,
    tags=["core", "connections"],
) as dag:

    t0 = PythonOperator(
        task_id="add_conn",
        python_callable=add_conn,
    )

    t1 = PythonOperator(
        task_id="check_uri_generation",
        python_callable=check_uri_gen,
    )


t0 >> t1
