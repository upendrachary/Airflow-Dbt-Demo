from __future__ import annotations

from datetime import datetime
import csv
import io
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

S3_BUCKET = os.environ.get("INSURANCE_S3_BUCKET", "your-s3-bucket")
S3_PREFIX = os.environ.get("INSURANCE_S3_PREFIX", "insurance_claims")
SNOWFLAKE_STAGE = os.environ.get("INSURANCE_SNOWFLAKE_STAGE", "RAW_S3_STAGE")
DBT_PROJECT_DIR = "/opt/airflow/dbt_insurance"
DBT_PROFILES_DIR = f"{DBT_PROJECT_DIR}/profiles"


def _write_csv(rows: list[dict], headers: list[str]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def generate_and_upload_to_s3() -> None:
    hook = S3Hook(aws_conn_id="aws_default")

    policies = [
        {
            "policy_id": "POL-1001",
            "customer_id": "CUST-001",
            "product": "Gold",
            "start_date": "2023-01-01",
            "end_date": "2024-12-31",
            "premium": 425.50,
        },
        {
            "policy_id": "POL-1002",
            "customer_id": "CUST-002",
            "product": "Silver",
            "start_date": "2023-06-01",
            "end_date": "2024-05-31",
            "premium": 310.00,
        },
    ]

    members = [
        {
            "member_id": "MEM-1001",
            "customer_id": "CUST-001",
            "dob": "1985-05-12",
            "gender": "F",
            "city": "Denver",
            "state": "CO",
        },
        {
            "member_id": "MEM-1002",
            "customer_id": "CUST-002",
            "dob": "1978-11-02",
            "gender": "M",
            "city": "Austin",
            "state": "TX",
        },
    ]

    providers = [
        {
            "provider_id": "PR-9001",
            "provider_type": "Hospital",
            "npi": "1234567890",
            "city": "Denver",
            "state": "CO",
        },
        {
            "provider_id": "PR-9002",
            "provider_type": "Clinic",
            "npi": "9876543210",
            "city": "Austin",
            "state": "TX",
        },
    ]

    claims = [
        {
            "claim_id": "CL-5001",
            "policy_id": "POL-1001",
            "member_id": "MEM-1001",
            "provider_id": "PR-9001",
            "claim_dt": "2024-08-20 12:00:00",
            "billed_amt": 1250.00,
            "paid_amt": 975.50,
            "status": "APPROVED",
        },
        {
            "claim_id": "CL-5002",
            "policy_id": "POL-1002",
            "member_id": "MEM-1002",
            "provider_id": "PR-9002",
            "claim_dt": "2024-08-22 08:30:00",
            "billed_amt": 830.00,
            "paid_amt": 0.00,
            "status": "PENDING",
        },
    ]

    claim_lines = [
        {
            "claim_line_id": "CLL-7001",
            "claim_id": "CL-5001",
            "cpt_code": "99213",
            "diagnosis_code": "Z00.00",
            "line_amt": 500.00,
        },
        {
            "claim_line_id": "CLL-7002",
            "claim_id": "CL-5001",
            "cpt_code": "93000",
            "diagnosis_code": "I10",
            "line_amt": 750.00,
        },
        {
            "claim_line_id": "CLL-7003",
            "claim_id": "CL-5002",
            "cpt_code": "99214",
            "diagnosis_code": "R51",
            "line_amt": 830.00,
        },
    ]

    datasets = {
        "policy": (policies, list(policies[0].keys())),
        "member": (members, list(members[0].keys())),
        "provider": (providers, list(providers[0].keys())),
        "claim": (claims, list(claims[0].keys())),
        "claim_line": (claim_lines, list(claim_lines[0].keys())),
    }

    for table, (rows, headers) in datasets.items():
        csv_body = _write_csv(rows, headers)
        key = f"{S3_PREFIX}/{table}/{table}.csv"
        hook.load_string(
            string_data=csv_body,
            key=key,
            bucket_name=S3_BUCKET,
            replace=True,
        )


with DAG(
    dag_id="insurance_claims_snowflake",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["snowflake", "dbt", "insurance"],
) as dag:
    generate_s3_files = PythonOperator(
        task_id="generate_s3_files",
        python_callable=generate_and_upload_to_s3,
    )

    copy_into_raw = SnowflakeOperator(
        task_id="snowflake_copy_into_raw",
        snowflake_conn_id="snowflake_default",
        sql=[
            "copy into raw.policy from @{{ params.stage }}/policy/ file_format=(type=csv skip_header=1) pattern='.*\\.csv';",
            "copy into raw.member from @{{ params.stage }}/member/ file_format=(type=csv skip_header=1) pattern='.*\\.csv';",
            "copy into raw.provider from @{{ params.stage }}/provider/ file_format=(type=csv skip_header=1) pattern='.*\\.csv';",
            "copy into raw.claim from @{{ params.stage }}/claim/ file_format=(type=csv skip_header=1) pattern='.*\\.csv';",
            "copy into raw.claim_line from @{{ params.stage }}/claim_line/ file_format=(type=csv skip_header=1) pattern='.*\\.csv';",
        ],
        params={"stage": SNOWFLAKE_STAGE},
    )

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=(
            f"DBT_PROFILES_DIR={DBT_PROFILES_DIR} "
            f"dbt debug --project-dir {DBT_PROJECT_DIR}"
        ),
    )

    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=(
            f"DBT_PROFILES_DIR={DBT_PROFILES_DIR} "
            f"dbt snapshot --project-dir {DBT_PROJECT_DIR}"
        ),
    )

    dbt_run_core = BashOperator(
        task_id="dbt_run_core",
        bash_command=(
            f"DBT_PROFILES_DIR={DBT_PROFILES_DIR} "
            f"dbt run --project-dir {DBT_PROJECT_DIR} --select path:models/staging path:models/core"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"DBT_PROFILES_DIR={DBT_PROFILES_DIR} "
            f"dbt test --project-dir {DBT_PROJECT_DIR}"
        ),
    )

    dbt_run_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command=(
            f"DBT_PROFILES_DIR={DBT_PROFILES_DIR} "
            f"dbt run --project-dir {DBT_PROJECT_DIR} --select path:models/marts"
        ),
    )

    generate_s3_files >> copy_into_raw >> dbt_debug >> dbt_snapshot >> dbt_run_core
    dbt_run_core >> dbt_test >> dbt_run_marts
