
  
    

  create  table "analytics"."public"."hello_dbt__dbt_tmp"
  
  
    as
  
  (
    select
    'hello from dbt running in Docker Desktop' as message,
    current_timestamp as generated_at
  );
  