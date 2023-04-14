from ow_forecast_calculators import ow_chance_rain
from nws_forecast_calculators_3hr import nws_chance_rain_3hr


def chance_rain_average(lat: str, long: str, hours: int):
    ow_acc_output = ow_chance_rain(lat, long, hours)
    nws_acc_output = nws_chance_rain_3hr(lat, long, hours)
    ow_pop_per_period = ow_acc_output['ow_pop_tracker']
    nws_pop_per_period = nws_acc_output['nws_chance_rain_3hr']
    pop_average_per_3hr = []
    for period in range(len(nws_pop_per_period)):
        ow_nws_sum = (ow_pop_per_period[period] * 100) + nws_pop_per_period[period]
        ow_nws_average = ow_nws_sum / 2
        pop_average_per_3hr.append(ow_nws_average)
    return {'pop_average_per_3hr': pop_average_per_3hr}
