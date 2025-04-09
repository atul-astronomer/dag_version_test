from airflow.decorators import dag, task


@dag()
def simple_dynamic_task_mapping():
    @task
    def get_nums():
        return [1, 2, 3]  # A

    @task
    def times_2(num):  # B
        return num * 2

    @task
    def add_10(num):  # C
        return num + 10

    _get_nums = get_nums()
    _times_2 = times_2.expand(num=_get_nums)  # D
    add_10.expand(num=_times_2)  # E


simple_dynamic_task_mapping()  # F
