

select distinct
    event_type,
    initcap(replace(event_type, '_', ' ')) as event_type_label
from "analytics"."public"."raw_events"