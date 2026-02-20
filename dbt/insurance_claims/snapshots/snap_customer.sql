{% snapshot snap_customer %}

{{
    config(
      target_schema='core',
      unique_key='customer_id',
      strategy='check',
      check_cols=['date_of_birth', 'gender', 'city', 'state']
    )
}}

select
    customer_id,
    date_of_birth,
    gender,
    city,
    state
from {{ ref('stg_member') }}

{% endsnapshot %}
