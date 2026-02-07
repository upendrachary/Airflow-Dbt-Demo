{{ config(materialized='table') }}

select distinct
    event_type,
    initcap(replace(event_type, '_', ' ')) as event_type_label
from {{ source('app', 'raw_events') }}
