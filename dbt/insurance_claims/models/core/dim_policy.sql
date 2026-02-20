select
    policy_id,
    customer_id,
    product,
    start_date,
    end_date,
    premium
from {{ ref('stg_policy') }}
