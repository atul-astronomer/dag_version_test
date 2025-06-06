from datetime import datetime

from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import Asset
from airflow.sdk.definitions.asset import Dataset, Model

from airflow.decorators import dag
from airflow.utils.trigger_rule import TriggerRule
from dags.plugins.airflow_dag_introspection import assert_the_task_states
from airflow.providers.standard.operators.python import PythonOperator

# these two will have downstream dags
left = Asset(name='asset_name', uri='asset_uri2', group='ABC')
right = Dataset(uri="asset_uri")
centre = Model(name="model_asset")


@dag(start_date=datetime(1970, 1, 1), schedule=None, tags=["asset", "AIP-74"])
def test_asset_creation():
    l = EmptyOperator(task_id="left", outlets=[left])
    c = EmptyOperator(task_id="center", outlets=[centre])
    r = EmptyOperator(task_id="right", outlets=[right])
    status = PythonOperator(
        task_id="assert_task_status",
        python_callable=assert_the_task_states,
        op_args=[{
            "left": "success",
            "right": "success",
            "center": "success"
        }],
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )
    l >> r >> c >> status


test_asset_creation()
