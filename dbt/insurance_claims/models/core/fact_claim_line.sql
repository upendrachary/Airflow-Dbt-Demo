{{
    config(
        materialized='incremental',
        unique_key='claim_line_id',
        incremental_strategy='merge'
    )
}}

with base as (
    select
        claim_line_id,
        claim_id,
        cpt_code,
        diagnosis_code,
        line_amt
    from {{ ref('stg_claim_line') }}
)

select *
from base

{% if is_incremental() %}
    where claim_line_id not in (select claim_line_id from {{ this }})
{% endif %}
