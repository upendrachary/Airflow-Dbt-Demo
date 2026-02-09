with source_data as (
    select *
    from {{ source('raw', 'claim_line') }}
)

select
    cast(claim_line_id as varchar) as claim_line_id,
    cast(claim_id as varchar) as claim_id,
    trim(cpt_code) as cpt_code,
    trim(diagnosis_code) as diagnosis_code,
    cast(line_amt as number(12,2)) as line_amt
from source_data
