select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select event_type_label
from "analytics"."public"."dim_event_types"
where event_type_label is null



      
    ) dbt_internal_test