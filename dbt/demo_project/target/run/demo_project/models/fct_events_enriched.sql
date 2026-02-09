
      
        
            delete from "analytics"."public"."fct_events_enriched"
            where (
                event_id) in (
                select (event_id)
                from "fct_events_enriched__dbt_tmp180653407738"
            );

        
    

    insert into "analytics"."public"."fct_events_enriched" ("event_id", "event_type", "event_type_label", "occurred_at")
    (
        select "event_id", "event_type", "event_type_label", "occurred_at"
        from "fct_events_enriched__dbt_tmp180653407738"
    )
  