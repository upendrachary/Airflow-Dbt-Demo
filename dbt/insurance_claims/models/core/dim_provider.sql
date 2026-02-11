select
    provider_id,
    provider_type,
    npi,
    city,
    state
from {{ ref('stg_provider') }}
