import requests
import json
from enum import Enum
import math

points_endpoint = "https://api.weather.gov/points/{},{}"
open_weather_endpoint = "https://api.openweathermap.org/data/2.5/" \
                        "forecast?lat={}&lon={}&appid=9a20243a726eb799985560eb9ff039a2"


class SourceEnum(Enum):
    OPEN_WEATHER = 1
    NATIONAL_WEATHER_SERVICE = 2


class PrecipitationData:
    def __init__(self, hourly_precipitation_probability: list[float], three_hour_precipitation_probability: list[float],
                 three_hour_precipitation_accumulation: list[float], missing_data: bool, source: SourceEnum):
        self.hourly_precipitation_probability = hourly_precipitation_probability
        self.three_hour_precipitation_probability = three_hour_precipitation_probability
        self.three_hour_precipitation_accumulation = three_hour_precipitation_accumulation
        self.missing_data = missing_data
        self.source = source


def forecast_fetcher(lat: float, long: float, source: SourceEnum) -> list:
    if SourceEnum.OPEN_WEATHER == source:
        url = open_weather_endpoint
    else:
        url = points_endpoint

    response = requests.get(url.format(lat, long))
    response_json = json.loads(response.text)

    if source == SourceEnum.OPEN_WEATHER:
        return response_json["list"]
    elif source == SourceEnum.NATIONAL_WEATHER_SERVICE:
        cld_nws_parsed_properties = response_json['properties']
        canyon_nws_hourly_forecast = cld_nws_parsed_properties['forecastHourly']
        canyon_hourly_response = requests.get(canyon_nws_hourly_forecast)
        canyon_hourly_data = canyon_hourly_response.text
        parsed_canyon_hourly_data = json.loads(canyon_hourly_data)
        canyon_hourly_properties = parsed_canyon_hourly_data['properties']
        return canyon_hourly_properties['periods']


def read_nws_weather_response(forecast_list: list, hours: int) -> PrecipitationData:
    nws_chance_rain_missing_data = False
    nws_pop_tracker = []
    for i in range(hours):
        try:
            period_pop = forecast_list[i]['probabilityOfPrecipitation']
            nws_pop_tracker.append(period_pop['value'])
        except KeyError:
            nws_chance_rain_missing_data = True
            break
    nws_pop_per_3hr = []
    for i in range(math.ceil(hours / 3)):
        try:
            three_hour_sum = nws_pop_tracker[i] + \
                             nws_pop_tracker[i + 1] + \
                             nws_pop_tracker[i + 2]
            three_hour_average = three_hour_sum / 3
            nws_pop_per_3hr.append(three_hour_average)
        except IndexError:
            nws_chance_rain_missing_data = True
            break
    return PrecipitationData(nws_pop_tracker, nws_pop_per_3hr, None,
                             nws_chance_rain_missing_data, SourceEnum.NATIONAL_WEATHER_SERVICE)


def read_open_weather_response(forecast_list: list, hours: int) -> PrecipitationData:
    ow_missing_data = False
    ow_inches_per_period = []
    for i in range(math.ceil(hours / 3)):
        try:
            period_accum = forecast_list[i]['rain']
            inches_accum = period_accum['3h'] / 25.4
            ow_inches_per_period.append(inches_accum)
        except KeyError:
            ow_missing_data = True
            break
    ow_pop_tracker = []  # pop stands for probability of precipitation
    for i in range(math.ceil(hours / 3)):
        try:
            current_period = forecast_list[i]['pop']
            ow_pop_tracker.append(current_period)
        except KeyError:
            ow_missing_data = True
            break
    return PrecipitationData(None, ow_pop_tracker, ow_inches_per_period,
                             ow_missing_data, SourceEnum.OPEN_WEATHER)

