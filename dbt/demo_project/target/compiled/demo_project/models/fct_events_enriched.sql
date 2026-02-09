

select
    events.event_id,
    events.event_type,
    types.event_type_label,
    events.occurred_at
from "analytics"."public"."fct_events" as events
left join "analytics"."public"."dim_event_types" as types
    on events.event_type = types.event_type


  where events.occurred_at > (select max(occurred_at) from "analytics"."public"."fct_events_enriched")
