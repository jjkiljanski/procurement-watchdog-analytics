{% macro dev_date_window(column_name) -%}
  {% set date_from = var('dev_date_from', none) %}
  {% set date_to = var('dev_date_to', none) %}

  {% if date_from is not none or date_to is not none %}
    where 1 = 1
    {% if date_from is not none %}
      and cast({{ column_name }} as date) >= cast('{{ date_from }}' as date)
    {% endif %}
    {% if date_to is not none %}
      and cast({{ column_name }} as date) <= cast('{{ date_to }}' as date)
    {% endif %}
  {% endif %}
{%- endmacro %}
