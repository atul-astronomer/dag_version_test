from airflow.sdk import DAG
from airflow.providers.standard.operators.python import BranchPythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from pendulum import today

from providers.standard.src.airflow.providers.standard.operators.empty import EmptyOperator

with DAG(
    dag_id="skip_mixin_task",
    default_args={"owner": "airflow", "start_date": today('UTC').add(days=-2)},
    schedule=None,
    tags=["core"],
) as dag:

    def needs_some_extra_task(some_bool_field, **kwargs):
        if some_bool_field:
            return f"extra_task"
        else:
            return f"final_task"

    branch_op = BranchPythonOperator(
        task_id=f"branch_task",
        python_callable=needs_some_extra_task,
        op_kwargs={"some_bool_field": True},  # For purposes of showing the problem
    )

    # will be always ran in this example
    extra_op = EmptyOperator(
        task_id=f"extra_task",
    )
    extra_op.set_upstream(branch_op)

    # should not be skipped
    final_op = EmptyOperator(
        task_id="final_task",
        trigger_rule="none_failed",
    )
    final_op.set_upstream([extra_op, branch_op])
