import os
import pandas as pd
from psycopg2.extras import execute_values
from db_connection import get_db_connection     


# City-Station mapping
# https://www.ncei.noaa.gov/maps/daily/
station_to_city = {
     72055399999: "new_york",
     72202012839: "miami",
     99849999999: "chicago",
     72278023183: "phoenix",
     72793524234: "seattle",
     72565003017: "denver",
     72288593197: "los_angeles",
     72059400188: "houston",
     72658014922: "minneapolis",
     72484653123: "las_vegas"
}

def load_csv_to_postgres(csv_file_path, conn):
    """
    Load CSV into PostgreSQL, inserting new data and updating changes.
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    df['city'] = df['STATION'].map(station_to_city)

    # Rename columns to match the table structure
    df = df.rename(columns={
        'STATION': 'station_id',
        'DATE': 'date',
        'NAME': 'name',
        'TEMP': 'temp',
        'DEWP': 'dewp',
        'WDSP': 'wdsp',
        'MAX': 'max_temp',
        'MIN': 'min_temp',
        'PRCP': 'prcp'
    })

    # Connect to PostgreSQL and insert data
    with conn.cursor() as cur:
        # Define insert query with ON CONFLICT to handle duplicates
        insert_query = """
        INSERT INTO staging_weather (station_id, date, name, city, temp, dewp, wdsp, max_temp, min_temp, prcp)
        VALUES %s
        ON CONFLICT (station_id, date) DO UPDATE
        SET name = EXCLUDED.name
        temp = EXCLUDED.temp,
        dewp = EXCLUDED.dewp,
        wdsp = EXCLUDED.wdsp,
        max_temp = EXCLUDED.max_temp,
        min_temp = EXCLUDED.min_temp,
        prcp = EXCLUDED.prcp;
        """
        values = [tuple(row) for row in df[['station_id', 'date', 'name', 'city', 'temp', 'dewp', 'wdsp', 'max_temp', 'min_temp', 'prcp']].values]

        # Insert multiple rows at once
        execute_values(cur, insert_query, values)
        conn.commit()  

    print(f"Data from {csv_file_path} loaded successfully!")


def load_all_csvs_to_postgres():
    conn = get_db_connection()
    # absolute path - inside container
    csv_folder_path = '/opt/weather_pipeline/data' 
    try:
        with get_db_connection() as conn:
            for filename in os.listdir(csv_folder_path):
                csv_file_path = os.path.join(csv_folder_path, filename)
                load_csv_to_postgres(csv_file_path, conn)

    except Exception as e:
        print(f"Database connection error: {e}")
