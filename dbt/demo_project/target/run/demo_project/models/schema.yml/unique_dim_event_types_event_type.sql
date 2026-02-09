select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    event_type as unique_field,
    count(*) as n_records

from "analytics"."public"."dim_event_types"
where event_type is not null
group by event_type
having count(*) > 1



      
    ) dbt_internal_test