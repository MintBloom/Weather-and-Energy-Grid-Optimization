import requests
import pandas as pd

def get_current_weather_data(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    return data

def get_historic_weather_data(latitude, longitude, start_date, end_date):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,snowfall_sum,wind_speed_10m_max"
    response = requests.get(url)
    data = response.json()
    return data

data_historic = get_historic_weather_data(51.5085, -0.1257, "2025-06-20", "2026-06-20")
print(data_historic)

data_current = get_current_weather_data(51.5085, -0.1257)
print(f"\n{data_current}")
