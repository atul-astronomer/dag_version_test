from airflow.decorators import dag, task
from airflow.models.param import Param

from datetime import datetime, timedelta

docs = """
# Purpose

Checks that the JSON 'string' or python str datatype interfaces with the dag parameter 'params'.
It does this by asserting that the type of the data passed through to the function is the type that was passed in with 'params'.
Additionally the function fail_if_invalid makes sure that the character length of the string is between 2 and 23
The pattern keyword argument is a regex search that matches everything so it should always pass.

## Steps

1. Unpause
2. Wait for dag run to complete
3. Trigger a new dagrun without config
4. Trigger a new dagrun with config, but make no changes
5. Trigger a new dagrun with config, but change it to be some other valid value (any string with a character length between 2 and 23)
    - Ensure that the key remains as "a" so the task can make an assertion on its datatype\n
    - Examples:\n
            {"a": "coffee"}
            {"a": "donuts"}
            {"a": "muffins"}
            {"a" "9fj0m68k2l71if1sczi5"}
6. Trigger a new dagrun with config, but change it to be some invalid value (any datatype other than a string)
    - Examples:\n
            {"a": 34}
            {"a": [1, "ted", 2, "tee"]}
            {"a": {"new_dict": "some_value"}}

## Expectations

- **2 - 5**: All tasks succeed
- **6**: The dagrun is never created, user sees validation error in UI or gets error via API
"""

@task
def fail_if_invalid(val):
        print(val)
        assert type(val) == str
        # since the value being overridden is static should I just assert for the value?
        # assert val is "hello qa-team"    


@dag(
    start_date=datetime(2021, 1, 1),
    schedule=timedelta(days=365, hours=6),
    params={
        "a": Param(
            "3tHjh32k9l8q", type="string", minLength=2, maxLength=23, pattern="[\s\S]"
        )
    },
    doc_md=docs,
    tags=["core", "taskflow-api", "dagparams"],
)
def string_params_taskflow(string):
    fail_if_invalid(string)

dag = string_params_taskflow("hello qa-team!")