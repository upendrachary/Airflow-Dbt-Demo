
  
    

  create  table "analytics"."public"."dim_event_types__dbt_tmp"
  
  
    as
  
  (
    

select distinct
    event_type,
    initcap(replace(event_type, '_', ' ')) as event_type_label
from "analytics"."public"."raw_events"
  );
  