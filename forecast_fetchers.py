import requests
import json

# Try to generalize these endpoints and their usages. I'd expect both the endpoints and functions to 
# receive latitude and longitude as parameters. 
# Then usages can be simplified so that the same sort of logic is applied. 
# i.e. 
# def fx(lat: float, long: float, source: SourceEnumType) -> ClassYouDefine:
#     url =  SourceEnum.OPEN_WEATHER == source ? open_weather_endpoint : points_endpoint;

#     response = requests.get(url.format(lat, long))
#     response_json = json.loads(response.text)

#     if (source == SourceEnum.OPEN_WEATHER):
#         return read_open_weather_response(response_json)
#     elif (source == SourceEnum.NATIONAL_WEATHER_SERVICE):
#         return read_national_weather_service_response(response_json)

points_endpoint = "https://api.weather.gov/points/"
open_weather_endpoint = "https://api.openweathermap.org/data/2.5/" \
                        "forecast?lat={lat}&lon={long}&appid=9a20243a726eb799985560eb9ff039a2"


# Canyon cords is a magic thing here, the contracts of functions should be well defined.
# What is the function receiving, if it relies on a certain format, what is that contract?
# Strong typing alone isn't enough in some cases, we need to explain in comments the expected behavior
def canyon_forecast_fetcher_nws(canyon_cords):
    canyon_nws_endpoint = points_endpoint + canyon_cords
    canyon_nws_location_response = requests.get(canyon_nws_endpoint)
    canyon_nws_location_data = canyon_nws_location_response.text
    cld_nws_parsed = json.loads(canyon_nws_location_data)  # cld stands for canyon location data
    cld_nws_parsed_properties = cld_nws_parsed['properties']
    canyon_nws_hourly_forecast = cld_nws_parsed_properties['forecastHourly']
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
    open_weather_lat = open_weather_endpoint.replace("{lat}", lat)
    open_weather_final_endpoint = open_weather_lat.replace("{long}", long)
    print(open_weather_final_endpoint)  # remove these later
    open_weather_response = requests.get(open_weather_final_endpoint)
    open_weather_data = open_weather_response.text
    owd_parsed = json.loads(open_weather_data)  # owd stands for open weather data
    return owd_parsed["list"]
