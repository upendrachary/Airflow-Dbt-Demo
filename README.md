# Airflow + dbt Demo (Beginner to Advanced)

If you are new to **Apache Airflow** and **dbt**, this repository is designed to help you learn both tools step by step.

## What you will learn

- Airflow basics: DAGs, tasks, scheduling, and operators.
- dbt basics: models, sources, tests, and documentation.
- How Airflow orchestrates dbt runs.
- Practical patterns for production-ready analytics pipelines.

## Suggested learning path

1. **Start with fundamentals**
   - Understand what Airflow does vs what dbt does.
   - Learn how a simple DAG is defined.
   - Learn how a simple dbt model is built and run.

2. **Build integration basics**
   - Trigger dbt runs from Airflow.
   - Add data quality checks and task dependencies.
   - Configure schedules and retries.

3. **Move to intermediate workflows**
   - Use multiple environments (dev/staging/prod).
   - Parameterize DAGs and dbt commands.
   - Add alerts and observability.

4. **Advance to production patterns**
   - Modular DAG architecture.
   - CI/CD for dbt and Airflow deployments.
   - Backfills, incremental models, and performance tuning.

## How to use this repo effectively

- Start with the simplest examples first.
- Run each workflow end-to-end before moving on.
- Read logs in Airflow and docs in dbt for every run.
- Make small changes and re-run to understand behavior.

## For newcomers

It is completely normal to feel overwhelmed in the beginning. Focus on one concept at a time: first orchestration (Airflow), then transformation (dbt), then how they work together.

---

If you want, we can also add:
- a week-by-week study plan,
- a glossary of key terms,
- and troubleshooting notes for common setup issues.
