with source_data as (
    select *
    from {{ source('raw', 'policy') }}
)

select
    cast(policy_id as varchar) as policy_id,
    cast(customer_id as varchar) as customer_id,
    trim(product) as product,
    cast(start_date as date) as start_date,
    cast(end_date as date) as end_date,
    cast(premium as number(12,2)) as premium
from source_data
