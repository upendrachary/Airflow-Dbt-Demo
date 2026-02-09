with claims as (
    select *
    from {{ ref('fact_claim') }}
)

select
    cast(claim_timestamp as date) as claim_date,
    count(*) as total_claims,
    sum(billed_amt) as total_billed_amt,
    sum(paid_amt) as total_paid_amt,
    avg(case when status = 'APPROVED' then 1 else 0 end) as approval_rate,
    avg(datediff('day', claim_timestamp, current_timestamp())) as avg_processing_days
from claims
group by 1
