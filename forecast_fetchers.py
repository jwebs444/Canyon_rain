import requests
import json
points_endpoint = "https://api.weather.gov/points/"
open_weather_endpoint = "https://api.openweathermap.org/data/2.5/" \
                        "forecast?lat={lat}&lon={long}&appid=9a20243a726eb799985560eb9ff039a2"


def canyon_forecast_fetcher_nws(canyon_cords):
    canyon_nws_endpoint = points_endpoint + canyon_cords
    canyon_nws_location_response = requests.get(canyon_nws_endpoint)
    canyon_nws_location_data = canyon_nws_location_response.text
    cld_nws_parsed = json.loads(canyon_nws_location_data)  # cld stands for canyon location data
    cld_nws_parsed_properties = cld_nws_parsed['properties']
    canyon_nws_hourly_forecast = cld_nws_parsed_properties['forecastHourly']
    print(canyon_nws_hourly_forecast)  # remove these later
    canyon_hourly_response = requests.get(canyon_nws_hourly_forecast)
    canyon_hourly_data = canyon_hourly_response.text
    parsed_canyon_hourly_data = json.loads(canyon_hourly_data)
    canyon_hourly_properties = parsed_canyon_hourly_data['properties']
    return canyon_hourly_properties['periods']


def canyon_forecast_fetcher_ow(lat, long):
    open_weather_lat = open_weather_endpoint.replace("{lat}", lat)
    open_weather_final_endpoint = open_weather_lat.replace("{long}", long)
    print(open_weather_final_endpoint)  # remove these later
    open_weather_response = requests.get(open_weather_final_endpoint)
    open_weather_data = open_weather_response.text
    owd_parsed = json.loads(open_weather_data)  # owd stands for open weather data
    return owd_parsed["list"]
