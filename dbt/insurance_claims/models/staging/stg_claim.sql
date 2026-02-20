with source_data as (
    select *
    from {{ source('raw', 'claim') }}
)

select
    cast(claim_id as varchar) as claim_id,
    cast(policy_id as varchar) as policy_id,
    cast(member_id as varchar) as member_id,
    cast(provider_id as varchar) as provider_id,
    cast(claim_dt as timestamp_ntz) as claim_timestamp,
    cast(billed_amt as number(12,2)) as billed_amt,
    cast(paid_amt as number(12,2)) as paid_amt,
    upper(trim(status)) as status
from source_data
