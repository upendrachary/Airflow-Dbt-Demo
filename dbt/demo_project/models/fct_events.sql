{{ config(materialized='incremental', unique_key='event_id') }}

select
    event_id,
    event_type,
    occurred_at
from {{ source('app', 'raw_events') }}

{% if is_incremental() %}
  where occurred_at > (select max(occurred_at) from {{ this }})
{% endif %}
