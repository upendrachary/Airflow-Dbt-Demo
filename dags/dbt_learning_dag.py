from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PSQL_CONN = "host=postgres user=airflow password=airflow dbname=analytics"

with DAG(
    dag_id="dbt_learning_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dbt", "learning"],
) as dag:
    create_raw_events = BashOperator(
        task_id="create_raw_events",
        bash_command=(
            "psql '" + PSQL_CONN + "' -v ON_ERROR_STOP=1 -c \""
            "CREATE TABLE IF NOT EXISTS raw_events ("
            "event_id BIGINT PRIMARY KEY, "
            "event_type TEXT NOT NULL, "
            "occurred_at TIMESTAMPTZ NOT NULL"
            ");\""
        ),
    )

    load_new_events = BashOperator(
        task_id="load_new_events",
        bash_command=(
            "psql '" + PSQL_CONN + "' -v ON_ERROR_STOP=1 -c \""
            "INSERT INTO raw_events (event_id, event_type, occurred_at) "
            "SELECT (extract(epoch from now())::bigint * 1000) + gs, "
            "'page_view', now() "
            "FROM generate_series(1, 3) gs "
            "ON CONFLICT (event_id) DO NOTHING;\""
        ),
    )

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

    create_raw_events >> load_new_events >> dbt_debug >> dbt_run >> dbt_test
