import requests  # for api calling
import pandas as pd # for data manipulation into dataframes especially
from sqlalchemy import create_engine # for exporting data to postgreSQL db
from urllib import parse

def get_historic_weather_data(latitude, longitude, start_date, end_date):
    # gathering data from the open-meteo api
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

def get_energy_data():
    sql_query =  '''SELECT COUNT(*) OVER () AS _count, * FROM "f93d1835-75bc-43e5-84ad-12472b180a98" WHERE "HYDRO" >= '0' AND "SOLAR" >= '0' AND "WIND" >= '0' AND "DATETIME" >= '2025-06-10T00:00:00.000Z' AND "DATETIME" <= '2026-06-10T23:59:59.999Z' ORDER BY "_id" ASC LIMIT 100'''
    params = {'sql': sql_query}

    try:
        response = requests.get('https://api.neso.energy/api/3/action/datastore_search_sql', params = parse.urlencode(params))
        data = response.json()['result']
        print(data) # Printing data
    except requests.exceptions.RequestException as e:
        print(e.response.text)
    
def get_carbon_intensity_data():
    response = requests.get('https://api.carbonintensity.org.uk/regional/scotland')
    data = response.json()
    print(data)

def export_to_postgresql(username, password, host, port, database_name, df):
    # ----- exporting data the PostgreSQL database ------

    # username =   your username 
    # password =    password created during installation
    # host =       host name/address
    # port =        port number
    # database_name = "Weather and Energy Database" database name
    # df = dataframe to be exported

    engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}") 

    table_name = "history_weather_data" # table name you want to use/create
    df.to_sql(table_name, con=engine, if_exists="append", index=False)

    print("Data exported to PostgreSQL database successfully.")


if __name__ == "__main__":
    #df= get_historic_weather_data(51.5085, -0.1257, "2025-06-20", "2026-06-20")
    #print(df.head())  # check the first rows of the dataframe

    #export_to_postgresql("postgres", "", "localhost", "5432", "Weather and Energy Database", df)


    get_carbon_intensity_data()  
