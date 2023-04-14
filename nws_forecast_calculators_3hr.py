from nws_forecast_calculators_hourly import nws_chance_rain


def nws_chance_rain_3hr(lat: str, long: str, hours: int):
    nws_chance_rain_missing_data = False
    nws_chance_rain_output = nws_chance_rain(lat, long, hours)
    nws_pop_per_hour = nws_chance_rain_output['nws_pop_tracker']
    nws_pop_per_3hr = []
    tracking_time = 0
    while tracking_time < hours:
        try:
            three_hour_sum = nws_pop_per_hour[tracking_time] + \
                             nws_pop_per_hour[tracking_time+1] + \
                             nws_pop_per_hour[tracking_time+2]
            three_hour_average = three_hour_sum / 3
            nws_pop_per_3hr.append(three_hour_average)
            tracking_time += 3
        except IndexError:
            nws_chance_rain_missing_data = True
            break
    return {'nws_chance_rain_3hr': nws_pop_per_3hr, 'nws_chance_rain_missing_data': nws_chance_rain_missing_data}
