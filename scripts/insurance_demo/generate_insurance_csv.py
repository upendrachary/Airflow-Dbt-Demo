import csv
import pathlib
from datetime import date, datetime, timedelta

OUTPUT_DIR = pathlib.Path("./tmp/insurance_claims")


def write_csv(path, rows, headers):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    today = date.today()
    policies = [
        {
            "policy_id": "POL-1001",
            "customer_id": "CUST-001",
            "product": "Gold",
            "start_date": today - timedelta(days=365),
            "end_date": today + timedelta(days=365),
            "premium": 425.50,
        },
        {
            "policy_id": "POL-1002",
            "customer_id": "CUST-002",
            "product": "Silver",
            "start_date": today - timedelta(days=180),
            "end_date": today + timedelta(days=185),
            "premium": 310.00,
        },
    ]

    members = [
        {
            "member_id": "MEM-1001",
            "customer_id": "CUST-001",
            "dob": date(1985, 5, 12),
            "gender": "F",
            "city": "Denver",
            "state": "CO",
        },
        {
            "member_id": "MEM-1002",
            "customer_id": "CUST-002",
            "dob": date(1978, 11, 2),
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
            "claim_dt": datetime.now() - timedelta(days=3),
            "billed_amt": 1250.00,
            "paid_amt": 975.50,
            "status": "APPROVED",
        },
        {
            "claim_id": "CL-5002",
            "policy_id": "POL-1002",
            "member_id": "MEM-1002",
            "provider_id": "PR-9002",
            "claim_dt": datetime.now() - timedelta(days=1),
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

    write_csv(OUTPUT_DIR / "policy" / "policy.csv", policies, policies[0].keys())
    write_csv(OUTPUT_DIR / "member" / "member.csv", members, members[0].keys())
    write_csv(OUTPUT_DIR / "provider" / "provider.csv", providers, providers[0].keys())
    write_csv(OUTPUT_DIR / "claim" / "claim.csv", claims, claims[0].keys())
    write_csv(
        OUTPUT_DIR / "claim_line" / "claim_line.csv",
        claim_lines,
        claim_lines[0].keys(),
    )

    print(f"Wrote CSVs to {OUTPUT_DIR.resolve()}")
