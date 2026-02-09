select
    customer_id,
    date_of_birth,
    gender,
    city,
    state,
    dbt_valid_from,
    dbt_valid_to
from {{ ref('snap_customer') }}
