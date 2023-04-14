from forecast_fetchers import canyon_forecast_fetcher_nws


def nws_chance_rain(lat: str, long: str, hours: int):
    canyon_cords = lat + "," + long
    nws_chance_rain_missing_data = False
    canyon_hourly_periods = canyon_forecast_fetcher_nws(canyon_cords)
    tracking_period = 0
    nws_pop_tracker = []  # pop stands for probability of precipitation
    while tracking_period < hours:
        try:
            current_period = canyon_hourly_periods[tracking_period]
            period_pop = current_period['probabilityOfPrecipitation']
            nws_pop_tracker.append(period_pop['value'])
            tracking_period += 1
        except KeyError:
            nws_chance_rain_missing_data = True
            break
    nws_no_pop_forward = 0
    no_pop_backward = -1
    while nws_pop_tracker[nws_no_pop_forward] == 0:
        nws_no_pop_forward += 1
        if nws_no_pop_forward >= hours:
            break
    while nws_pop_tracker[no_pop_backward] == 0:
        no_pop_backward -= 1
        if nws_pop_tracker[no_pop_backward] != 0:
            no_pop_backward += 1
            break
        if hours + no_pop_backward < 1:
            break
    nws_hours_no_pop = 1 + hours + no_pop_backward
    return {'nws_pop_tracker': nws_pop_tracker, 'nws_hours_no_pop': nws_hours_no_pop,
            'nws_no_pop_forward': nws_no_pop_forward, 'nws_chance_rain_missing_data': nws_chance_rain_missing_data}
