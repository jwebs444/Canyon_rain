from forecast_fetchers import canyon_forecast_fetcher_ow
import math


def ow_accumulation_tracker(lat: str, long: str, hours: int):
    owd_list = canyon_forecast_fetcher_ow(lat, long)
    ow_acc_missing_data = False
    inches_tracker = 0
    ow_inches_per_period = []

    for i in range(math.ceil(hours/3)):
        current_period = owd_list[i]
        try:
            period_accum = current_period['rain']
            inches_accum = period_accum['3h'] / 25.4
            inches_tracker += inches_accum
            period_accum_string = str(inches_accum)
            period_accum_string_trim = period_accum_string[:5]
            ow_inches_per_period.append(period_accum_string_trim)
        except KeyError:
            ow_acc_missing_data = True
            break

        list = [2, 2, 2]
        list[3]
        
    inches_tracker_string = str(inches_tracker)
    ow_inches_tracker_trim = inches_tracker_string[:5]
    return {'ow_inches_tracker_trim': ow_inches_tracker_trim,
            'ow_inches_per_period': ow_inches_per_period,
            'ow_acc_missing_data': ow_acc_missing_data}


def ow_chance_rain(lat: str, long: str, hours: int):
    owd_list = canyon_forecast_fetcher_ow(lat, long)
    ow_chance_rain_missing_data = False
    tracking_index = 0
    tracking_time = 0
    ow_pop_tracker = []  # pop stands for probability of precipitation
    while tracking_time < hours:
        try:
            current_period = owd_list[tracking_index]
            period_pop = current_period['pop']
            ow_pop_tracker.append(period_pop)
        except KeyError:
            ow_chance_rain_missing_data = True
            break
        tracking_index += 1
        tracking_time += 3
    ow_no_pop_forward = 0
    no_pop_backward = -1
    time_forward = 0
    time_backward = hours
    while ow_pop_tracker[ow_no_pop_forward] == 0:
        ow_no_pop_forward += 1
        time_forward += 3
        if time_forward >= hours:
            break
    while ow_pop_tracker[no_pop_backward] == 0:
        no_pop_backward -= 1
        time_backward -= 3
        if ow_pop_tracker[no_pop_backward] != 0:
            no_pop_backward -= 1
            break
        if time_backward < 1:
            break
    return {'ow_3hour_pop_tracker': ow_pop_tracker,
            'ow_no_pop_after': time_backward,
            'ow_no_pop_forward': time_forward,
            'ow_chance_rain_missing_data': ow_chance_rain_missing_data}


def no_precipitation_after(probability_of_precipitation: int[]):


# nws_pop_tracker
# nws_hours_no_pop
# nws_no_pop_forward
# nws_chance_rain_missing_data

class CalculatedPrecipitation():
    def __init__(self, probability_of_precipitation, no_precipitation_after, no) -> None:
        pass