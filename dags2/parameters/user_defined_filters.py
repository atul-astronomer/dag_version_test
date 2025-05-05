from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from plugins.airflow_dag_introspection import log_checker

docs = """
####Purpose
This dag tests the 'user_defined_macros' dag parameter that allows the user to pipe python functions into bash commands.
####Expected Behavior
This dag has 2 tasks that are both expected to succeed. If either one or both tasks fail then there is a problem with 'user_defined_macros'.
"""

with DAG(
    dag_id="user_defined_filters",
    start_date=days_ago(1),
    schedule_interval=None,
    user_defined_filters=dict(hello=lambda name: "Hello %s" % name),
    doc_md=docs,
    tags=["dagparams"],
) as dag:
    templated_command = """
        echo {{"world" | hello}}
    """
    B0 = BashOperator(task_id="generate_hello_world", bash_command=templated_command)

    py0 = PythonOperator(
        task_id="check_the_logs",
        python_callable=log_checker,
        op_args=["generate_hello_world", "Hello world", "World hello"],
    )

B0 >> py0
