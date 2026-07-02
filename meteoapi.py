import requests  # for api calling
import pandas as pd # for data manipulation into dataframes especially
from sqlalchemy import create_engine # for exporting data to postgreSQL db


def get_historic_weather_data(latitude, longitude, start_date, end_date):
    # data gathered from the open-meteo api
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,snowfall_sum,wind_speed_10m_max"
    response = requests.get(url)
    data = response.json()
    
    daily = data["daily"]
    dataframe = pd.DataFrame(daily)

    dataframe = dataframe.rename(columns={"time": "date"}) #rename "time" column to "date"
    dataframe["date"] = pd.to_datetime(dataframe["date"])
    dataframe[latitude] = latitude
    dataframe[longitude] = longitude
    
    print(dataframe.head())  # check the first rows of the dataframe
    print(dataframe.info())  # checks the data types and non-null counts
    print(dataframe.isnull().sum())  # check for missing values

    
    return dataframe

df= get_historic_weather_data(51.5085, -0.1257, "2025-06-20", "2026-06-20")
print(df.head())  # check the first rows of the dataframe

# ----- exporting data the PostgreSQL database ------

username = "postgres" # your username 
password = ""       # password created during installation
host = "localhost"  # host name/address
port = "5432"       # port number
database_name = "Weather and Energy Database" # database name

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}") 

table_name = "history_weather_data" # table name you want to use/create
df.to_sql(table_name, con=engine, if_exists="append", index=False)

print("Data exported to PostgreSQL database successfully.")
