from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.date_time import DateTimeSensor


with DAG(
    "example_datetime_sensor",
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["sensor"],
) as dag:
    replace_hour = DateTimeSensor(
        task_id="60_secs_later",
        target_time="{{ ti.start_date + macros.timedelta(seconds=60) }}",
    )
