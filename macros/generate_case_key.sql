{% macro generate_case_key(columns) -%}
  md5(
    {% for column in columns %}
      coalesce(cast({{ column }} as {{ dbt.type_string() }}), '')
      {% if not loop.last %} || '|' || {% endif %}
    {% endfor %}
  )
{%- endmacro %}
