{% macro raw_silver_relation(table_name) -%}
  {% if target.type == 'duckdb' %}
    {{ ref('local_raw__' ~ table_name) }}
  {% else %}
    {{ source('raw_silver', table_name) }}
  {% endif %}
{%- endmacro %}
