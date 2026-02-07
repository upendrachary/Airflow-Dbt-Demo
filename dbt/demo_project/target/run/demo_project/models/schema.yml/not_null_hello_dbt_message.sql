select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select message
from "analytics"."public"."hello_dbt"
where message is null



      
    ) dbt_internal_test