{{ config(materialized='incremental', unique_key='event_id') }}

select
    events.event_id,
    events.event_type,
    types.event_type_label,
    events.occurred_at
from {{ ref('fct_events') }} as events
left join {{ ref('dim_event_types') }} as types
    on events.event_type = types.event_type

{% if is_incremental() %}
  where events.occurred_at > (select max(occurred_at) from {{ this }})
{% endif %}
