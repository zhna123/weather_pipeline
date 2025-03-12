import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  # default to localhost if not set
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)  # default to 5432 if not set

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

# PostgreSQL connection details
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT
)

def load_csv_to_postgres(csv_file_path):
    """
    Load CSV into PostgreSQL
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
        insert_query = """
        INSERT INTO staging_weather (station_id, date, name, city, temp, dewp, wdsp, max_temp, min_temp, prcp)
        VALUES %s
        """
        values = [tuple(row) for row in df[['station_id', 'date', 'name', 'city', 'temp', 'dewp', 'wdsp', 'max_temp', 'min_temp', 'prcp']].values]

        # Insert multiple rows at once
        execute_values(cur, insert_query, values)
        conn.commit()  

    print(f"Data from {csv_file_path} loaded successfully!")

# Load all CSV files
csv_folder_path = '../data' 
for filename in os.listdir(csv_folder_path):
      csv_file_path = os.path.join(csv_folder_path, filename)
      load_csv_to_postgres(csv_file_path)


conn.close()
