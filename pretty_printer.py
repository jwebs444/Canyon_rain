from forecast_fetchers import PrecipitationData
from nws_ow_3hr_average import chance_rain_average


def printer(data: PrecipitationData, hours: int, lat, long):
    print("")
    print(f"{hours} hour precipitation forecast for {lat},{long}")
    print(f"Forecast Source: {data.source.name}")
    print(f"Data Missing: {data.missing_data}")
    print("")
    if data.hourly_precipitation_probability is not None:
        print(f"Hourly Precipitation Chance: {data.hourly_precipitation_probability}")
    else:
        print(f"3hr Precipitation Chance:{data.three_hour_precipitation_probability}")
    if data.three_hour_precipitation_accumulation is not None:
        print(f"3hr Accumulation: {data.three_hour_precipitation_accumulation}")


def average_printer(ow_precipitation_data: PrecipitationData, nws_precipitation_data: PrecipitationData):
    print("")
    print(f"Three Hour Probability of Precipitation Average: "
          f"{chance_rain_average(ow_precipitation_data, nws_precipitation_data)}")
    print("")


