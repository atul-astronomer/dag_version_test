from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.sensors.date_time import DateTimeSensorAsync


with (DAG("async_trigger_sleep", schedule_interval=None, start_date=days_ago(1),tags=["async_migration"])
      ) as dag:
    DateTimeSensorAsync(
        task_id="wait_for_start",
        target_time=datetime(2028, 12, 10),

    )