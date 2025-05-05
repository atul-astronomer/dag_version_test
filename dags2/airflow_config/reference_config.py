from datetime import datetime
from textwrap import dedent

import airflow.configuration as conf
from airflow import DAG
from airflow.decorators import task


@task
def print_this(this):
    print(this)


with DAG(
    dag_id="config_ref",
    schedule=None,
    start_date=datetime(1970, 1, 1),
    doc_md=dedent(
        """
        Created For: https://github.com/apache/airflow/issues/27999
        
        This dag references some config values.
        If airflow renames those values, references to the old ones should still work.
        
        If something is wrong with the backwards compatibility layer, this dag will fail to parse.
        """
    ),
) as dag:

    namespace = conf.get("kubernetes", "NAMESPACE")
    # TODO: reference all the configs

    print_this(namespace)
