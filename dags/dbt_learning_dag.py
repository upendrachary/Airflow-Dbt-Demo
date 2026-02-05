from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dbt_learning_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dbt", "learning"],
) as dag:
    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command="cd /opt/airflow/dbt && dbt debug",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt && dbt test",
    )

    dbt_debug >> dbt_run >> dbt_test
