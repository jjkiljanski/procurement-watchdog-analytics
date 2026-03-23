{% macro regex_match(column_name, pattern) -%}
  {% if target.type == 'duckdb' %}
    regexp_full_match(cast({{ column_name }} as {{ dbt.type_string() }}), '{{ pattern }}')
  {% elif target.type == 'bigquery' %}
    regexp_contains(cast({{ column_name }} as string), r'{{ pattern }}')
  {% else %}
    regexp_like(cast({{ column_name }} as {{ dbt.type_string() }}), '{{ pattern }}')
  {% endif %}
{%- endmacro %}
