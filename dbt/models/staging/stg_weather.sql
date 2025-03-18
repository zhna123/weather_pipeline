{{ config(materialized='view') }}

SELECT 
    station_id,
    date,
    name,
    city,
    CAST(temp AS FLOAT) AS temp,
    CAST(dewp AS FLOAT) AS dewp,
    CAST(wdsp AS FLOAT) AS wdsp,
    CAST(max_temp AS FLOAT) AS max_temp,
    CAST(min_temp AS FLOAT) AS min_temp,
    CAST(prcp AS FLOAT) AS prcp
FROM {{ source('staging', 'staging_weather') }}
WHERE temp IS NOT NULL
