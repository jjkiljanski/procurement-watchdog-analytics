{% test matches_regex(model, column_name, pattern) %}
select
    {{ column_name }} as invalid_value
from {{ model }}
where {{ column_name }} is not null
  and not {{ regex_match(column_name, pattern) }}
{% endtest %}
