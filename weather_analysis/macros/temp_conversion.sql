{% macro celsius_to_fahrenheit(temp_col) %}
    ({{ temp_col }} * 9/5) + 32
{% endmacro %}
