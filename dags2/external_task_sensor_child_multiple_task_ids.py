from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.models import BaseOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskMarker, ExternalTaskSensor, ExternalTaskSensorLink
from airflow.utils.state import TaskInstanceState

from datetime import datetime, timedelta

docs = """
####Purpose
This dag is a simple dag whose only purpose is to be ran at a specific execution date so it can be checked by the ExternalTaskSensor.\n
The validity of the success of this dag comes from the ExternalTaskSensor checking the task_id's.
####Expected Behavior
All tasks expected to succeed.
"""

with DAG(
    dag_id="external_task_sensor_child_dag",
    start_date=datetime(2022, 3, 12, 3, 28, 0),
    schedule_interval=timedelta(days=1),
    is_paused_upon_creation=False,
    doc_md=docs,
    tags=["core", "sensor"],
) as dag:

    d0 = DummyOperator(task_id="child_dummy1")

    d2 = DummyOperator(task_id="child_dummy2")

d0 >> d2 

