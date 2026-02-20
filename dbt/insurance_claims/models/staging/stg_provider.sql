with source_data as (
    select *
    from {{ source('raw', 'provider') }}
)

select
    cast(provider_id as varchar) as provider_id,
    trim(provider_type) as provider_type,
    trim(npi) as npi,
    trim(city) as city,
    trim(state) as state
from source_data
