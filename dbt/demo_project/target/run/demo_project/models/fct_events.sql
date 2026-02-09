
      
        
            delete from "analytics"."public"."fct_events"
            where (
                event_id) in (
                select (event_id)
                from "fct_events__dbt_tmp180653035924"
            );

        
    

    insert into "analytics"."public"."fct_events" ("event_id", "event_type", "occurred_at")
    (
        select "event_id", "event_type", "occurred_at"
        from "fct_events__dbt_tmp180653035924"
    )
  