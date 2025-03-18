from db_connection import get_db_connection


def create_staging_table():
    """
    Creates the staging table if it does not exist.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS staging_weather (
      id SERIAL PRIMARY KEY,            -- Unique identifier for each record
      station_id VARCHAR(20) NOT NULL,  -- Station ID for each weather station
      date DATE NOT NULL,               -- Date of the recorded weather data
      name VARCHAR(100),                -- Raw station name from the CSV
      city VARCHAR(100),                -- City name for easy reference
      temp FLOAT,                       -- Temperature in Celsius (or as per the dataset)
      dewp FLOAT,                       -- Dew point temperature
      wdsp FLOAT,                       -- Wind speed
      max_temp FLOAT,                   -- Maximum temperature for the day
      min_temp FLOAT,                   -- Minimum temperature for the day
      prcp FLOAT                        -- Precipitation in inches or millimeters
    )
    """
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()
    print("Staging table created (if it didn’t exist).")
