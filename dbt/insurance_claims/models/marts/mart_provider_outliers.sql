with claims as (
    select *
    from {{ ref('fact_claim') }}
),

provider_rollup as (
    select
        provider_id,
        count(*) as total_claims,
        avg(case when status = 'DENIED' then 1 else 0 end) as deny_rate,
        avg(paid_amt / nullif(billed_amt, 0)) as paid_to_billed_ratio
    from claims
    group by 1
)

select
    provider_id,
    total_claims,
    deny_rate,
    paid_to_billed_ratio
from provider_rollup
where total_claims >= 5
  and (deny_rate >= 0.4 or paid_to_billed_ratio >= 1.1)
