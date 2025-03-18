{{ config(materialized='table') }}

WITH base_data AS (
    SELECT
        city,
        EXTRACT(YEAR FROM date) AS year,
        CASE 
            WHEN EXTRACT(MONTH FROM date) IN (12, 1, 2) THEN 'Winter'
            WHEN EXTRACT(MONTH FROM date) IN (3, 4, 5) THEN 'Spring'
            WHEN EXTRACT(MONTH FROM date) IN (6, 7, 8) THEN 'Summer'
            WHEN EXTRACT(MONTH FROM date) IN (9, 10, 11) THEN 'Fall'
        END AS season,
        temp,
        dewp,
        wdsp,
        max_temp,
        min_temp,
        prcp
    FROM {{ ref('stg_weather') }}
),

seasonal_averages AS (
    SELECT
        city,
        year,
        season,
        ROUND(AVG(temp)::NUMERIC, 2) AS avg_temp,
        ROUND(AVG(dewp)::NUMERIC, 2) AS avg_dewp,
        ROUND(AVG(wdsp)::NUMERIC, 2) AS avg_wdsp,
        ROUND(MAX(max_temp)::NUMERIC, 2) AS max_temp,
        ROUND(MIN(min_temp)::NUMERIC, 2) AS min_temp,
        ROUND(SUM(prcp)::NUMERIC, 2) AS total_prcp
    FROM base_data
    GROUP BY city, year, season
)

SELECT *
FROM seasonal_averages
