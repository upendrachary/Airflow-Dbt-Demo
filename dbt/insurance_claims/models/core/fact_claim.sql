{{
    config(
        materialized='incremental',
        unique_key='claim_id',
        incremental_strategy='merge'
    )
}}

with base as (
    select
        claim_id,
        policy_id,
        member_id as customer_id,
        provider_id,
        claim_timestamp,
        billed_amt,
        paid_amt,
        status
    from {{ ref('stg_claim') }}
)

select *
from base

{% if is_incremental() %}
    where claim_timestamp > (select coalesce(max(claim_timestamp), '1900-01-01'::timestamp_ntz) from {{ this }})
{% endif %}
