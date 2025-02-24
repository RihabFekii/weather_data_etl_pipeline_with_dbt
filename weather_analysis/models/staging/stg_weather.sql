{{ config(materialized='table') }}

SELECT
    city,
    DATE(timestamp) AS date,
    CAST(temperature AS FLOAT64) AS temperature_celsius,
    humidity,
    pressure,
    wind_speed
FROM {{ source('weather_data', 'weather_measurements') }}
WHERE temperature IS NOT NULL
