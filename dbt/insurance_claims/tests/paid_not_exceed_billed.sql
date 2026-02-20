{% test paid_not_exceed_billed(model, billed_field, paid_field) %}

select *
from {{ model }}
where {{ paid_field }} > {{ billed_field }}

{% endtest %}
