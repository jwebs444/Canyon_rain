from fastapi import FastAPI
from forecast_fetchers import read_nws_weather_response, read_open_weather_response, forecast_fetcher,SourceEnum
from nws_ow_3hr_average import chance_rain_average
from pretty_printer import printer, average_printer

"""
    TODO: 
        - Tests for functions, especially things that are trimming like lat[:5]
    How to make call
    http://127.0.0.1:8000/?lat={lat}&long={long}&hours={hours}
    
    Post is going to pass information to get
        
"""

app = FastAPI()


@app.get("/")
def home(lat: float, long: float, hours: int):
    nws_precipitation_data = read_nws_weather_response(
        forecast_fetcher(lat=lat, long=long, source=SourceEnum.NATIONAL_WEATHER_SERVICE), hours=hours)
    ow_precipitation_data = read_open_weather_response(
        forecast_fetcher(lat=lat, long=long, source=SourceEnum.OPEN_WEATHER), hours=hours)
    chance_average = chance_rain_average(ow_data=ow_precipitation_data, nws_data=nws_precipitation_data)
    # printer(nws_precipitation_data, hours=hours, lat=lat, long=long)
    # printer(ow_precipitation_data, hours=hours, lat=lat, long=long)
    # average_printer(ow_precipitation_data=ow_precipitation_data, nws_precipitation_data=nws_precipitation_data)
    return {
        "nws_precipitation_data": nws_precipitation_data,
        "ow_precipitation_data": ow_precipitation_data,
        "chance_rain_average": chance_average
    }


def test(lat: float, long: float, hours: int):
    nws_precipitation_data = read_nws_weather_response(
        forecast_fetcher(lat=lat, long=long, source=SourceEnum.NATIONAL_WEATHER_SERVICE), hours=hours)
    ow_precipitation_data = read_open_weather_response(
        forecast_fetcher(lat=lat, long=long, source=SourceEnum.OPEN_WEATHER), hours=hours)
    chance_rain_average(ow_data=ow_precipitation_data, nws_data=nws_precipitation_data)
    printer(nws_precipitation_data, hours=hours, lat=lat, long=long)
    printer(ow_precipitation_data, hours=hours, lat=lat, long=long)
    average_printer(ow_precipitation_data=ow_precipitation_data, nws_precipitation_data=nws_precipitation_data)


test(38, -109, 9)
