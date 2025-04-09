from __future__ import annotations

from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.triggers.file import FileDeleteTrigger
from airflow.sdk import Asset, AssetWatcher

from airflow.decorators import task, dag

# trigger = FileDeleteTrigger(filepath="/tmp/a")
# asset = Asset(
#     "test_asset_1", watchers=[AssetWatcher(name="file_watcher", trigger=trigger)]
# )


# with DAG(
#     dag_id="file_trigger_timeout",
#     start_date=datetime(2021, 1, 1),
#     catchup=False,
#     schedule=[asset],
# ) as dag:
#     t1 = EmptyOperator(task_id="t1")
#
#     t1


@dag(
    start_date=None,
    schedule=None,
    catchup=False,
)
def my_dag():

    @task(outlets=[Asset("a_NEW_asset2")])
    def my_task():
        pass

    my_task()


my_dag()
