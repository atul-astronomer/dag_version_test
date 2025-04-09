from datetime import timedelta

from airflow.sdk import DAG

from airflow.operators.bash import BashOperator
from airflow.timetables.trigger import CronTriggerTimetable
from pendulum import today
# from airflow.timetables.trigger import MultipleCronTriggerTimetable

default_args = {
    'owner': 'Atul',
    'start_date': today('UTC').add(days=-1)
}

# with DAG(dag_id='custom_timetable', default_args=default_args, schedule_interval='*/2 * * * *', max_active_runs=1, tags=['Atul']) as dag:
#
#     task_1 = BashOperator(task_id='task_1', bash_command='echo task 1')
#     task_2 = BashOperator(task_id='task_2', bash_command='echo task 2')
#
#     task_1 >> task_2
#
with DAG(
        dag_id='cron_timetable',
        default_args=default_args,
        schedule=CronTriggerTimetable(
            '*/1 * * * *',
            timezone='UTC',
            interval=timedelta(minutes=5)
        ),
        max_active_runs=1) as dag:

    task_1 = BashOperator(task_id='task_1', bash_command='echo task 1', pool='abc', pool_slots=2)
    task_2 = BashOperator(task_id='task_2', bash_command='echo task 2')

    task_1 >> task_2

# with DAG(
#         dag_id='multi_cron_timetable',
#         start_date=days_ago(1),
#         catchup=False,
#         schedule=MultipleCronTriggerTimetable(
#             '*/20 * * * *',
#             '*/1 * * * *',
#             timezone='UTC',
#             # interval=timedelta(minutes=5),
#             # run_immediately=True
#         ),
#         max_active_runs=1) as dag:
#
#     task_1 = BashOperator(task_id='task_1', bash_command='echo task 1')
#     task_2 = BashOperator(task_id='task_2', bash_command='echo task 2')
#
#     task_1 >> task_2
