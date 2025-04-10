from datetime import datetime, timedelta

from airflow.sdk import Asset
from airflow.sdk.definitions.asset.metadata import Metadata
# from airflow.sdk.metadata import Metadata
from airflow.decorators import task
from airflow.sdk import DAG

outlet = Asset('asset_outlet')
ten_days_ago = datetime.now() - timedelta(days=10)

with DAG(
    dag_id="test_asset_event_producer",
    start_date=ten_days_ago,
    schedule='@daily',
    tags=["asset", "AIP-74"],
    is_paused_upon_creation=False,
    catchup=True
) as dag:
    @task(outlets=[outlet])
    def asset_with_extra_by_yield():
        yield Metadata(outlet, {"hi": "bye"})

    asset_with_extra_by_yield()

with DAG(
    dag_id="test_asset_event_consumer",
    catchup=False,
    start_date=datetime.min,
    schedule=None,
    tags=["asset", "AIP-74"],
):

    @task(inlets=[outlet])
    def read_dataset_event(*, inlet_events=None):
        for event in inlet_events[outlet]:
            print("Event: ", event)
            print(event.extra["hi"])

    read_dataset_event()

