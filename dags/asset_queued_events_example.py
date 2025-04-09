from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import random

# Function to simulate asset event creation
def create_asset_event(event_type, **kwargs):
    asset_id = random.randint(1000, 9999)
    event = {
        "asset_id": asset_id,
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
    }
    # Simulate enqueueing event (replace with actual queue code, e.g., SQS or Kafka)
    print(f"Enqueued event: {event}")

# Default DAG arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# Instantiate the DAG
with DAG(
    "asset_event_queue_dag",
    default_args=default_args,
    description="A DAG to enqueue asset-related events",
    schedule=timedelta(hours=1),
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["assets", "events"],
) as dag:

    # Task to enqueue a "created" event
    enqueue_created_event = PythonOperator(
        task_id="enqueue_created_event",
        python_callable=create_asset_event,
        op_kwargs={"event_type": "created"},
    )

    # Task to enqueue an "updated" event
    enqueue_updated_event = PythonOperator(
        task_id="enqueue_updated_event",
        python_callable=create_asset_event,
        op_kwargs={"event_type": "updated"},
    )

    # Task to enqueue a "deleted" event
    enqueue_deleted_event = PythonOperator(
        task_id="enqueue_deleted_event",
        python_callable=create_asset_event,
        op_kwargs={"event_type": "deleted"},
    )

    # Define task dependencies
    enqueue_created_event >> enqueue_updated_event >> enqueue_deleted_event
