from __future__ import annotations

from airflow.decorators import dag, task
from airflow.sdk import Asset
from airflow.sdk.definitions.asset.decorators import asset

from providers.standard.src.airflow.providers.standard.operators.empty import EmptyOperator


@asset(uri="s3://bucket/asset11_producer", schedule=None)
def producer1():
    pass


@asset(uri="s3://bucket/asset2_producer", schedule=None)
def producer2():
    pass

@asset(uri="abc", schedule=None)
def producer3():
    pass


@dag(
    schedule=Asset.ref(name="asset11_producer") & Asset.ref(name="asset2_producer"),
    catchup=False,
    tags=["asset"],
)
def consumer():
    @task()
    def process_nothing(triggering_asset_events):
        for a, events in triggering_asset_events.items():
            print(a.name, events)
    task1 = EmptyOperator(task_id='task1')

    process_nothing() >> task1


consumer()

