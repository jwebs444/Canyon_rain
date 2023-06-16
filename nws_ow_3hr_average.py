from forecast_fetchers import PrecipitationData


def chance_rain_average(ow_data: PrecipitationData, nws_data: PrecipitationData) -> list:
    ow_pop_per_period = ow_data.three_hour_precipitation_probability
    nws_pop_per_period = nws_data.three_hour_precipitation_probability
    pop_average_per_3hr = []
    for index in range(len(nws_pop_per_period)):
        ow_nws_sum = (ow_pop_per_period[index] * 100) + nws_pop_per_period[index]
        ow_nws_average = ow_nws_sum / 2
        pop_average_per_3hr.append(ow_nws_average)
    return pop_average_per_3hr
