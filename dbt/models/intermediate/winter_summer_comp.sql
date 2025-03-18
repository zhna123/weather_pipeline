-- Winter vs. Summer Comparison of each city each year

{{ config(materialized='table') }}

WITH seasonal_avg AS (
    SELECT
        city,
        EXTRACT(YEAR FROM date) AS year,
        CASE
            WHEN EXTRACT(MONTH FROM date) IN (12, 1, 2) THEN 'Winter'
            WHEN EXTRACT(MONTH FROM date) IN (6, 7, 8) THEN 'Summer'
        END AS season,
        AVG(temp) AS avg_temp
    FROM {{ ref('stg_weather') }}
    WHERE EXTRACT(MONTH FROM date) IN (12, 1, 2, 6, 7, 8) -- Winter & Summer
    GROUP BY city, season, year
)
SELECT
    city,
    year,
    AVG(CASE WHEN season = 'Winter' THEN avg_temp END) AS winter_avg,
    AVG(CASE WHEN season = 'Summer' THEN avg_temp END) AS summer_avg
FROM seasonal_avg
GROUP BY city, year
ORDER BY city, year
