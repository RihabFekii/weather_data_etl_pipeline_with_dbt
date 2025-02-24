{{ config(materialized='table') }}

WITH daily_temps AS (
    SELECT
        city,
        date,
        AVG(temperature_celsius) AS avg_temp_celsius,
        {{ celsius_to_fahrenheit('AVG(temperature_celsius)') }} AS avg_temp_fahrenheit,
        MIN(temperature_celsius) AS min_temp,
        MAX(temperature_celsius) AS max_temp
    FROM {{ ref('stg_weather') }}
    GROUP BY city, date
)
SELECT
    dt.city,
    dt.date,
    dt.avg_temp_celsius,
    dt.avg_temp_fahrenheit,
    dt.max_temp - dt.min_temp AS temp_variation,
FROM daily_temps dt

