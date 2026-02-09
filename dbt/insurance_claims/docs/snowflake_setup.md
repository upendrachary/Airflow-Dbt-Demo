# Snowflake setup (Insurance Claims demo)

Use this as a checklist for your Snowflake trial account.

## 1) Create database + schemas

```sql
create database if not exists INSURANCE;
create schema if not exists INSURANCE.RAW;
create schema if not exists INSURANCE.STAGING;
create schema if not exists INSURANCE.CORE;
create schema if not exists INSURANCE.MARTS;
```

## 2) Create raw tables

```sql
use database INSURANCE;
use schema RAW;

create or replace table policy (
  policy_id string,
  customer_id string,
  product string,
  start_date date,
  end_date date,
  premium number(12,2)
);

create or replace table member (
  member_id string,
  customer_id string,
  dob date,
  gender string,
  city string,
  state string
);

create or replace table provider (
  provider_id string,
  provider_type string,
  npi string,
  city string,
  state string
);

create or replace table claim (
  claim_id string,
  policy_id string,
  member_id string,
  provider_id string,
  claim_dt timestamp_ntz,
  billed_amt number(12,2),
  paid_amt number(12,2),
  status string
);

create or replace table claim_line (
  claim_line_id string,
  claim_id string,
  cpt_code string,
  diagnosis_code string,
  line_amt number(12,2)
);
```

## 3) Create an external stage (S3)

```sql
create or replace stage raw_s3_stage
  url='s3://YOUR_BUCKET/insurance_claims/'
  storage_integration = YOUR_STORAGE_INTEGRATION
  file_format = (type=csv field_delimiter=',' skip_header=1);
```

> If you don't have a storage integration yet, follow the Snowflake docs for
> creating one, then grant your Snowflake role access to it.

## 4) Copy data into raw tables

```sql
copy into policy
from @raw_s3_stage/policy/
file_format=(type=csv skip_header=1)
pattern='.*\.csv';

copy into member
from @raw_s3_stage/member/
file_format=(type=csv skip_header=1)
pattern='.*\.csv';

copy into provider
from @raw_s3_stage/provider/
file_format=(type=csv skip_header=1)
pattern='.*\.csv';

copy into claim
from @raw_s3_stage/claim/
file_format=(type=csv skip_header=1)
pattern='.*\.csv';

copy into claim_line
from @raw_s3_stage/claim_line/
file_format=(type=csv skip_header=1)
pattern='.*\.csv';
```
