from __future__ import annotations

import pendulum
# from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import Asset

from airflow.models.dag import DAG
from providers.standard.src.airflow.providers.standard.operators.python import PythonOperator

dag1_asset = Asset("s3://dag1/output_1.txt", extra={"hi": "bye"}, group="ML Model")
dag1_asset_2 = Asset("s3://dag1/output_2.txt", extra={"hi": "bye"}, group="ML Model")
dag2_asset = Asset("s3://dag2/output_2.txt", extra={"hi": "bye"}, group="Dataset")


def func(**context):
    print("kfb", context)
    print("kfb", context.get("logical_date"))


with DAG(
    dag_id="asset_produces_1",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    tags=["produces", "asset-scheduled"],
) as dag1:
    PythonOperator(outlets=[dag1_asset_2, dag1_asset], task_id="producing_task_11", python_callable=func)

with DAG(
    dag_id="asset_produces_2",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    tags=["produces", "asset-scheduled"],
) as dag2:
    PythonOperator(task_id="producing_task_1231", python_callable=func, outlets=[dag2_asset])

with DAG(
    dag_id="asset_produces_3",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[dag1_asset_2, dag2_asset],
    tags=["produces", "asset-scheduled"],
) as dag2:
    PythonOperator(task_id="producing_task_1231", python_callable=func)
