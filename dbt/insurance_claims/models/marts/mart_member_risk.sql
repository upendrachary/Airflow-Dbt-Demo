with claims as (
    select *
    from {{ ref('fact_claim') }}
)

select
    customer_id,
    count(*) as total_claims,
    sum(billed_amt) as total_billed_amt,
    sum(paid_amt) as total_paid_amt,
    case when count(*) >= 3 then true else false end as high_claim_frequency
from claims
group by 1
