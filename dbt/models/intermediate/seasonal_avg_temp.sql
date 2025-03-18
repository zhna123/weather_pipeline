-- Seasonal Temperature Analysis (Seasonal Averages)

/*
  Assigns each date to a season (Winter, Spring, Summer, Fall).
  Calculates the average temperature for each city in each season.
*/

{{ config(materialized='table') }}

SELECT
    city,
    EXTRACT(YEAR FROM date) AS year,
    CASE
        WHEN EXTRACT(MONTH FROM date) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM date) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM date) IN (6, 7, 8) THEN 'Summer'
        WHEN EXTRACT(MONTH FROM date) IN (9, 10, 11) THEN 'Fall'
    END AS season,
    AVG(temp) AS avg_temp
FROM {{ ref('stg_weather') }}
GROUP BY city, season, year
ORDER BY city, year, season
