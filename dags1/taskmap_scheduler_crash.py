from __future__ import annotations

from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.sensors.date_time import DateTimeSensorAsync
from airflow.utils import timezone

with DAG(
    dag_id="file_trigger_expand_crash_1",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    schedule=None,
) as dag:
    instant = timezone.datetime(2026, 11, 22)
    task = DateTimeSensorAsync.partial(task_id="async", poke_interval=3).expand(
        target_time=[str(instant + timedelta(seconds=3)), str(instant + timedelta(seconds=10))]
    )

    task
