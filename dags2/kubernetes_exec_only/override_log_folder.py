from airflow.models import DAG
from airflow.operators.python import PythonVirtualenvOperator
from airflow.utils.dates import days_ago
from kubernetes.client import models as k8s

def callable_virtualenv():
    """
    Example function that will be performed in a virtual environment.

    Importing at the module level ensures that it will not attempt to import the
    library before it is installed.
    """
    from time import sleep

    from colorama import Back, Fore, Style

    print(Fore.RED + "some red text")
    print(Back.GREEN + "and with a green background")
    print(Style.DIM + "and in dim text")
    print(Style.RESET_ALL)
    for _ in range(10):
        print(Style.DIM + "Please wait...", flush=True)
        sleep(10)
    print("Finished")


with DAG(
    dag_id="test_logfolder",
    default_args={"owner": "airflow"},
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["k8s_exe"],
) as dag:

    task = PythonVirtualenvOperator(
        task_id="test_logfolder",
        python_callable=callable_virtualenv,
        requirements=["colorama==0.4.0"],
        system_site_packages=False,
        executor_config={
        "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            resources=k8s.V1ResourceRequirements(
                                requests={
                                   "cpu": 1,
                                    "memory": "500Mi",
                                },
                                limits={
                                    "cpu": 1,
                                    "memory": "500Mi",
                                }
                            ),
                        env=[k8s.V1EnvVar(name="AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER", value="s3://buckets/log-folder-jn/log"),
                                 k8s.V1EnvVar(name="AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID", value="test-connection")]
                        ),
                    ],
                )
            )
        }
    )
