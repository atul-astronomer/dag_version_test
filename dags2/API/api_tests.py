import os

from airflow.models import DAG
from airflow.decorators import task
import json
from airflow.utils.dates import days_ago
import subprocess

with DAG(
        dag_id="api_tests",
        start_date=days_ago(1),
        schedule_interval=None,
        catchup=False,
        tags=['api']
) as dag:
    env_file = "/usr/local/airflow/dags/API/environment_template.json"
    env_file_updated = "/usr/local/airflow/dags/API/environment_template_update.json"
    postman_collection = "/usr/local/airflow/dags/API/postman_collection.json"
    result_path = "/usr/local/airflow/include/result.txt"
    bearer_token = ""
    if "cloud.astronomer-stage.io" in os.environ['AIRFLOW__ASTRONOMER__CLOUD_UI_URL']:
        bearer_token = os.environ["STAGE_ORG_TOKEN"]
    elif "cloud.astronomer-dev.io" in os.environ['AIRFLOW__ASTRONOMER__CLOUD_UI_URL']:
        bearer_token = os.environ["dev_org_token"]


    @task
    def run_api_test():
        # Open the JSON file for reading
        with open(env_file, 'r') as file:
            data = json.load(file)

        # Make the replacements
        data['values'][0]['value'] = f"{os.environ['AIRFLOW__WEBSERVER__BASE_URL']}/api/v1/"

        data['values'][1]['value'] = bearer_token

        # Save the modified data back to the file
        with open(env_file_updated, 'w') as file:
            json.dump(data, file, indent=4)

        print("JSON file has been updated.")
        data = subprocess.run(["newman", "run", postman_collection, "-e", env_file_updated], capture_output=True,
                              text=True)
        print(data.stdout)
        return data.stdout


    run_api_test()
