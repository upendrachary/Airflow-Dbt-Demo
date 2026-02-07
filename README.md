# Airflow + dbt Demo (Learn by Running Locally on Docker Desktop)

Great idea. This repo is now set up so you can **learn Airflow and dbt by running everything locally** with Docker Desktop.

## What you get in this project

- Airflow services in Docker (`webserver`, `scheduler`, `init`) using a custom Airflow image with dbt installed.
- PostgreSQL in Docker for both:
  - Airflow metadata database (`airflow` DB), and
  - dbt target database (`analytics` DB).
- A beginner DAG that simulates a tiny “real-time” pipeline:
  1. create a raw events table
  2. insert new events
  3. `dbt debug`
  4. `dbt run`
  5. `dbt test`
- A minimal dbt project with:
  - a hello model
  - an incremental fact model (`fct_events`)
  - tests on the output

---

## Prerequisites

- Docker Desktop installed and running.
- At least ~4 GB RAM allocated to Docker Desktop.
- Ports available on your machine:
  - `8081` for Airflow UI
  - `5432` for PostgreSQL

---

## Project structure

```text
.
├── airflow/
│   ├── Dockerfile
│   └── requirements.txt
├── dags/
│   └── dbt_learning_dag.py
├── dbt/
│   └── demo_project/
│       ├── dbt_project.yml
│       ├── models/
│       │   ├── fct_events.sql
│       │   ├── hello_dbt.sql
│       │   └── schema.yml
│       └── profiles/
│           └── profiles.yml
├── postgres-init/
│   └── 01-create-analytics-db.sql
└── docker-compose.yml
```

---

## One-time setup (first run)

Run these commands from repo root:

```bash
# 1) Build images

docker compose build

# 2) Initialize Airflow DB and create admin user
# username: admin
# password: admin

docker compose run --rm airflow-init
```

If step 2 fails once, run it again (sometimes first startup timing causes retries).

---

## Start the stack

```bash
docker compose up -d postgres airflow-webserver airflow-scheduler
```

Check status:

```bash
docker compose ps
```

Open Airflow UI:

- URL: http://localhost:8081
- Username: `admin`
- Password: `admin`

---

## Run your first Airflow + dbt DAG

1. In Airflow UI, find DAG: **`dbt_learning_dag`**.
2. Turn it ON.
3. Click **Trigger DAG**.
4. Open Graph view and inspect task logs in this order:
   - `create_raw_events`
   - `load_new_events`
   - `dbt_debug`
   - `dbt_run`
   - `dbt_test`

You should see successful dbt execution in logs.

---

## What this DAG builds (plain language)

- **`raw_events`**: a raw table created by Airflow and filled with a few new rows each run.
- **`fct_events`**: an incremental dbt model that copies new raw events into a fact table.
- **Tests** ensure:
  - `event_id` is unique and not null,
  - `occurred_at` is not null.

This simulates a tiny real-time pipeline: Airflow loads new events, dbt transforms and tests them.

---

## Verify output in PostgreSQL (recommended)

Run this from your terminal:

```bash
docker compose exec postgres psql -U airflow -d analytics -c "select count(*) from raw_events;"

docker compose exec postgres psql -U airflow -d analytics -c "select count(*) from fct_events;"

# optional: see the last 5 rows

docker compose exec postgres psql -U airflow -d analytics -c "select * from fct_events order by occurred_at desc limit 5;"
```

---

## Run dbt directly in a dbt container (CLI learning mode)

If you want to practice dbt commands directly (outside Airflow):

```bash
docker compose --profile tools run --rm dbt dbt debug

docker compose --profile tools run --rm dbt dbt run

docker compose --profile tools run --rm dbt dbt test
```

This helps you learn dbt independently, then compare how Airflow orchestrates the same flow.

---

## Helpful day-to-day commands

```bash
# Stop services

docker compose down

# Stop + remove volumes (fresh reset; deletes local Postgres data)

docker compose down -v

# View Airflow scheduler logs

docker compose logs -f airflow-scheduler

# View Airflow webserver logs

docker compose logs -f airflow-webserver
```

---

## Beginner learning roadmap (clean progression)

1. **Learn Airflow basics first**
   - DAG, task, schedule, retries, logs.
2. **Learn dbt basics second**
   - model, profile, run, test.
3. **Connect both**
   - Understand how DAG tasks wrap dbt commands.
4. **Experiment**
   - Add a second model in `dbt/demo_project/models/`.
   - Add a schema test in `schema.yml`.
   - Add a new Airflow task for `dbt docs generate`.
5. **Advance later**
   - multiple environments (dev/prod), alerts, CI/CD.

---

## Common issues and quick fixes

- **Port 8080 already in use**
  - Stop the process using 8080 or remap port in `docker-compose.yml`.
- **Port 5432 already in use**
  - Stop local PostgreSQL or remap port.
- **Airflow UI not reachable immediately**
  - Wait 20–40 seconds and check: `docker compose logs -f airflow-webserver`.
- **DAG missing in UI**
  - Confirm file exists: `dags/dbt_learning_dag.py`.
  - Restart scheduler: `docker compose restart airflow-scheduler`.
- **`Could not read served logs: 403 FORBIDDEN`**
  - Cause: Airflow webserver and scheduler did not share the same `webserver.secret_key`.
  - Fix (already configured in this repo): `AIRFLOW__WEBSERVER__SECRET_KEY` is now pinned in `docker-compose.yml`.
  - If you ran old containers before this fix, reset and start fresh:
    ```bash
    docker compose down -v
    docker compose build
    docker compose run --rm airflow-init
    docker compose up -d postgres airflow-webserver airflow-scheduler
    ```
- **`dbt debug` fails with `Error from git --help`**
  - Cause: `dbt debug` expects `git` to be available inside the Airflow container.
  - Fix in this repo: Airflow image now installs `git` in `airflow/Dockerfile`.
  - Apply the fix locally by rebuilding and restarting:
    ```bash
    docker compose down -v
    docker compose build --no-cache
    docker compose run --rm airflow-init
    docker compose up -d postgres airflow-webserver airflow-scheduler
    ```

---

If you want next, I can add a **Week-1 to Week-4 practice plan** in this same repo so you can learn in structured daily tasks.
