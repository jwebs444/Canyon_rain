import requests
import json
from typing import Type

from enum import Enum

# Try to generalize these endpoints and their usages. I'd expect both the endpoints and functions to 
# receive latitude and longitude as parameters. 
# Then usages can be simplified so that the same sort of logic is applied. 
# i.e. 


points_endpoint = "https://api.weather.gov/points/{},{}"
open_weather_endpoint = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=9a20243a726eb799985560eb9ff039a2"

class SourceEnum(Enum):
    OPEN_WEATHER = 1
    NATIONAL_WEATHER_SERVICE = 2 

class PrecipitationData():
    "Precipiataion Data has stuff"

    def __init(self, hourly_precipitation_probability: list[float], three_hour_precipitation_probability: list[float], three_hour_precipitation_accumulation: list[float]):
        raise


def fx(lat: float, long: float, source: SourceEnumType) -> PrecipitationData:
    url = open_weather_endpoint if (SourceEnum.OPEN_WEATHER == source) else points_endpoint;

    response = requests.get(url.format(lat, long))
    response_json = json.loads(response.text)

    if (source == SourceEnum.OPEN_WEATHER):
        return read_open_weather_response(response_json)
    elif (source == SourceEnum.NATIONAL_WEATHER_SERVICE):
        return read_national_weather_service_response(response_json)
    

def read_open_weather_response(json_payload: json) -> PrecipitationData:
    # Fun Special Logic
    nws_pop_tracker = []
    
    while tracking_period < hours:
        try:
            period_pop = canyon_hourly_periods[tracking_period]['probabilityOfPrecipitation']
            nws_pop_tracker.append(period_pop['value'])
            tracking_period += 1
        except KeyError:
            nws_chance_rain_missing_data = True
            break


    
    # Fun new Special Logic
    return PrecipitationData(nws_pop_tracker, 2, 3)



def read_national_weather_service_response(json_payload: json) -> PrecipitationData:
    # Fun Special Logic
    return PrecipitationData(None, 2, 3)




# APP = (Get Data From Source && Process) ->
#  Transform Data -> 
#  Display


# Canyon cords is a magic thing here, the contracts of functions should be well defined.
# What is the function receiving, if it relies on a certain format, what is that contract?
# Strong typing alone isn't enough in some cases, we need to explain in comments the expected behavior
def canyon_forecast_fetcher_nws(lat, long):
    canyon_nws_endpoint = points_endpoint.format(lat, long)
    canyon_nws_location_response = requests.get(canyon_nws_endpoint)
    cld_nws_parsed = json.loads(canyon_nws_location_response.text)  # cld stands for canyon location data
    canyon_nws_hourly_forecast = cld_nws_parsed['properties']['forecastHourly']
    # Or don't use prints so you don't remove later, when something is useful to have around, stick it into a logger!
    # > import logging
    # > logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.WARN)
    # Then any useful print messages can be printed as a debug message
    # > logging.debug('Whatever message you want')
    # And you can set the logging level in basicConfig to logging.DEBUG to see the messages
    print(canyon_nws_hourly_forecast)  # remove these later
    canyon_hourly_response = requests.get(canyon_nws_hourly_forecast)
    canyon_hourly_data = canyon_hourly_response.text
    parsed_canyon_hourly_data = json.loads(canyon_hourly_data)
    canyon_hourly_properties = parsed_canyon_hourly_data['properties']
    return canyon_hourly_properties['periods']


def canyon_forecast_fetcher_ow(lat, long):
    open_weather_final_endpoint =  open_weather_endpoint.format(lat, long)
    print(open_weather_final_endpoint)  # remove these later
    open_weather_response = requests.get(open_weather_final_endpoint)
    open_weather_data = open_weather_response.text
    owd_parsed = json.loads(open_weather_data)  # owd stands for open weather data
    return owd_parsed["list"]
