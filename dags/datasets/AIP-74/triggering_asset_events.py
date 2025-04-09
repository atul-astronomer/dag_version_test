from pendulum import today
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import Asset
from airflow.sdk import DAG

from airflow.decorators import task
from dags.plugins.elephantsql_kashin import conn_id as postgres_conn_id

example_snowflake_asset = Asset("example_asset")

with DAG(dag_id="load_snowflake_data", schedule="@daily", start_date=today('UTC').add(days=-2)) as dag:
    task1 = SQLExecuteQueryOperator(
        task_id="load",
        conn_id=postgres_conn_id,
        outlets=[example_snowflake_asset],
        sql="select name from asset limit 5"
    )
    task1

with DAG(dag_id="query_snowflake_data", schedule=[example_snowflake_asset]):
    SQLExecuteQueryOperator(
        task_id="query",
        conn_id=postgres_conn_id,
        sql="""
          SELECT *
          FROM my_db.my_schema.my_table
          WHERE "updated_at" >= '{{ (triggering_asset_events.values() | first | first).source_dag_run.data_interval_start }}'
          AND "updated_at" < '{{ (triggering_asset_events.values() | first | first).source_dag_run.data_interval_end }}';
        """,
    )

    @task
    def print_triggering_asset_events(triggering_asset_events=None):
        for asset, asset_list in triggering_asset_events.items():
            print(asset, asset_list)
            print(asset_list[0].source_dag_run.dag_id)

    print_triggering_asset_events()
