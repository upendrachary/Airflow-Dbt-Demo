with source_data as (
    select *
    from {{ source('raw', 'member') }}
)

select
    cast(member_id as varchar) as member_id,
    cast(customer_id as varchar) as customer_id,
    cast(dob as date) as date_of_birth,
    upper(trim(gender)) as gender,
    trim(city) as city,
    trim(state) as state
from source_data
