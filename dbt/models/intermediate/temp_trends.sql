-- Temperature Trends Over Time

/*
  calculate the year-over-year change in average temperature for each city.
*/

{{ config(materialized='table') }}

WITH city_yearly_avg AS (
    SELECT
        city,
        EXTRACT(YEAR FROM date) AS year,
        AVG(temp) AS avg_temp
    FROM {{ ref('stg_weather') }}
    GROUP BY city, year
)
SELECT
    city,
    year,
    avg_temp,
    LAG(avg_temp) OVER (PARTITION BY city ORDER BY year) AS prev_year_avg,
    (avg_temp - LAG(avg_temp) OVER (PARTITION BY city ORDER BY year)) AS temp_change
FROM city_yearly_avg
ORDER BY city, year
