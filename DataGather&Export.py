import requests         # for api calling
import pandas as pd     # for data manipulation into dataframes especially
from sqlalchemy import create_engine # for exporting data to postgreSQL db
import os               # for reading files and directories

def get_historic_weather_data(latitude, longitude, start_date, end_date):
    # gathering data from the open-meteo api
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,precipitation,rain,snowfall,wind_speed_10m,shortwave_radiation,cloudcover&timezone=GMT"
    response = requests.get(url)
    data = response.json()
    
    hourly = data["hourly"]
    dataframe = pd.DataFrame(hourly)

    dataframe = dataframe.rename(columns={"time": "datetime"}) #rename "time" column to "date"
    dataframe["datetime"] = pd.to_datetime(dataframe["datetime"])
    dataframe["latitude"] = latitude
    dataframe["longitude"] = longitude
    
    print(dataframe.head())  # check the first rows of the dataframe
    print(dataframe.info())  # checks the data types and non-null counts
    print(dataframe.isnull().sum())  # check for missing values
    
    return dataframe



def read_demand_data_from_csvfile(file_path): # file_path is the path to the CSV file containing demand data
    # ----- reading demand data from a CSV file -----
    
    obj = os.scandir(file_path)
    energy_demand_dataframes = [] 
    for entry in obj:
        if entry.is_file() and entry.name.endswith('.csv'):
            print(entry.name)
            file = pd.read_csv(file_path + "\\" + entry.name, quotechar='"')            
            df = pd.DataFrame(file)
            df["SETTLEMENT_DATE"] = pd.to_datetime(df["SETTLEMENT_DATE"], format="%d/%m/%Y") # convert the settlement_date column format to datetime
            df = df.rename(columns={df.columns[2]: "ND"}) # name the third column as ND (National Demand)
            df["SETTLEMENT_PERIOD"] = pd.to_numeric(df["SETTLEMENT_PERIOD"]) # convert the settlement_period column to numeric
            
            df["datetime"] = df["SETTLEMENT_DATE"] + pd.to_timedelta((df["SETTLEMENT_PERIOD"] - 1) * 30, unit="m") # combine settlement_date and settlement_period columns into a single datetime column
            df_hourly = df.set_index(["SETTLEMENT_DATE", "SETTLEMENT_PERIOD"]) # create a composite key index
            df_hourly = df[df["SETTLEMENT_PERIOD"] % 2 == 1].copy() # extract hourly data and drop the half-hourly data (this line can be removed if half-hourly data is needed)

            print(df.shape)  # show the columns and rows of the dataframe
            print(df.dtypes)  # check the data types of the columns
            print(df.head())  # check the first rows of the dataframe
            print(df.isnull().sum())  # check for missing values
            df_hourly.to_csv('energy-demand-data\\' + "new_" + entry.name, index=False) # saving the dataframe to a new CSV file in the energy_demand_dataframes folder
            energy_demand_dataframes.append(df) # adding the new dataframe to the list of dataframes
            print(f"{entry.name} converted to csv")
    
    return energy_demand_dataframes


def combine_demand_dataframes(list_of_dataframes):
    
    final_df  = pd.concat(list_of_dataframes) # concatenate all the dataframes in the list into a single dataframe

    print(final_df.head()) 
    print(final_df.shape) 
    print(final_df["SETTLEMENT_DATE"].min(), final_df["SETTLEMENT_DATE"].max())  # check the minimum and maximum dates in the 
    final_df.to_csv('energy-demand-data\\' + "concatenated_demand_data.csv", index=False)
    return final_df


def export_to_postgresql(username, password, host, port, database_name, df, table_name):
    # exporting data the PostgreSQL database

    # username =   your username 
    # password =    password created during installation
    # host =       host name/address
    # port =       port number
    # database_name = "Weather and Energy Database" database name
    # df = dataframe to be exported
    # table_name = "history_weather_data" # table name you want to use/create
    
    engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}") 
    
    df.to_sql(table_name, con=engine, if_exists="append", index=False)

    print("Data exported to PostgreSQL database successfully.")
    

if __name__ == "__main__":
    historic_weather_df = get_historic_weather_data(51.5085, -0.1257, "2020-01-01", "2026-06-30") # fetch weather data and assemble into dataframe
    export_to_postgresql("postgres", "", "localhost", "5432", "Weather and Energy Database", historic_weather_df, "history_weather_data") # export dataframe to sql database

    energy_demand_df = read_demand_data_from_csvfile(r"C:\Users\asteg\Code\Github\Weather-and-Energy-Grid-Optimization\raw-energy-demand-data") # read energy data from csv and assemble into dataframe, substitute with your own file path
    combined_demand_df = combine_demand_dataframes(energy_demand_df) # concatenate all the dataframes into one dataframe
    export_to_postgresql("postgres", "", "localhost", "5432", "Weather and Energy Database", combined_demand_df, "energy_demand_data") # export dataframe to sql database
