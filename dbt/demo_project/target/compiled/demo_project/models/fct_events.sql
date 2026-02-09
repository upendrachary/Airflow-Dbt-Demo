

select
    event_id,
    event_type,
    occurred_at
from "analytics"."public"."raw_events"


  where occurred_at > (select max(occurred_at) from "analytics"."public"."fct_events")
