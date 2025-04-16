from __future__ import annotations

from airflow.sdk import dag, task


@dag
def example_simplest_dag():
    @task
    def my_task():
        pass

    my_task()

    @task
    def my_task2():
        pass

    my_task2()

    # @task
    # def my_task3():
    #     pass
    #
    # my_task3()


example_simplest_dag()