from fastapi import FastAPI
from ow_forecast_calculators import ow_accumulation_tracker, ow_chance_rain
from nws_forecast_calculators_hourly import nws_chance_rain
from nws_ow_3hr_average import chance_rain_average
from forecast_fetchers import fx, SourceEnum, PrecipitationData

"""
    TODO: 
        - Tests for functions, especially things that are trimming like lat[:5]
    How to make call
    http://127.0.0.1:8000/?lat={lat}&long={long}&hours={hours}

"""

app = FastAPI()

# Rather than a bunch of data just kinda strung along, look into giving your response structure
# i.e.  you could create a class with descriptive names for the various dictionaries it'd contain
#       then if you json.dumps() your object so the api has a structured response/contract


@app.get("/")
def home(lat: str, long: str, hours: int):
    nw_data = fx(lat, long, SourceEnum.NATIONAL_WEATHER_SERVICE)
    ow_data = fx(lat, long, SourceEnum.OPEN_WEATHER)
    return PrettyOutput.prettyPrintWeatherData(nw_data, ow_data)



class PrettyOutput:

    class Output:
        def __init__(self, national_weather_service_data, ow, no_rain_nw, no_rain_ow) -> None:
            self.national_weather_service_data = national_weather_service_data
            self.open_weather_data = ow
            pass
    
    def prettyPrintWeatherData(nw_data: PrecipitationData, ow_data: PrecipitationData) -> str:
        nw_chance_after = chance_after(nw_data)
        ow_chance_after = chance_after(ow_data)
        return json.dumps(Output(nw_data, ow_data, nw_chance_after, ow_chance_after))

