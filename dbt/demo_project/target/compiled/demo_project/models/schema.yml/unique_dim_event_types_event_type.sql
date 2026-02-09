
    
    

select
    event_type as unique_field,
    count(*) as n_records

from "analytics"."public"."dim_event_types"
where event_type is not null
group by event_type
having count(*) > 1


