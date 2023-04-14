from fastapi import FastAPI
from ow_forecast_calculators import ow_accumulation_tracker, ow_chance_rain
from nws_forecast_calculators_hourly import nws_chance_rain
from nws_ow_3hr_average import chance_rain_average

"""
    TODO: 
        - Tests for functions, especially things that are trimming like lat[:5]
    How to make call
    http://127.0.0.1:8000/?lat={lat}&long={long}&hours={hours}

"""

app = FastAPI()


@app.get("/")
def home(lat: str, long: str, hours: int):
    ow_acc_output = ow_accumulation_tracker(lat, long, hours)
    ow_pop_output = ow_chance_rain(lat, long, hours)
    nws_pop_output = nws_chance_rain(lat, long, hours)
    average_output = chance_rain_average(lat, long, hours)
    return ow_pop_output, ow_acc_output, nws_pop_output, average_output