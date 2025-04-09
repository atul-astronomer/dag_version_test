from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
# from airflow.operators.latest_only import LatestOnlyOperator
from pendulum import today

from providers.standard.src.airflow.providers.standard.operators.latest_only import LatestOnlyOperator

dag = DAG(
    dag_id="latest_only",
    schedule=None,
    start_date=today('UTC').add(days=-2),
    tags=["core"],
)

latest_only = LatestOnlyOperator(task_id="latest_only", dag=dag)
task1 = EmptyOperator(task_id="task1", dag=dag)

latest_only >> task1
