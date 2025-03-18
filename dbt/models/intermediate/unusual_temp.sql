-- Identify Unusually Warm/Cold Years

/*
  calculate the standard deviation and then flag years that 
  deviate significantly from the average.
*/

{{ config(materialized='table') }}

WITH city_yearly_avg AS (
    SELECT
        city,
        EXTRACT(YEAR FROM date) AS year,
        AVG(temp) AS avg_temp
    FROM {{ ref('stg_weather') }}
    GROUP BY city, year
),
city_avg_and_sd AS (
    SELECT
        city,
        AVG(avg_temp) AS avg_temp_overall,
        STDDEV(avg_temp) AS sd_temp
    FROM city_yearly_avg
    GROUP BY city
)
SELECT
    cya.city,
    cya.year,
    cya.avg_temp,
    c.avg_temp_overall,
    c.sd_temp,
    CASE
        WHEN cya.avg_temp > c.avg_temp_overall + c.sd_temp THEN 'Unusually Warm'
        WHEN cya.avg_temp < c.avg_temp_overall - c.sd_temp THEN 'Unusually Cold'
        ELSE 'Normal'
    END AS temperature_anomaly
FROM city_yearly_avg cya
JOIN city_avg_and_sd c
    ON cya.city = c.city
ORDER BY cya.city, cya.year
