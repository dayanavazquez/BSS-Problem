from Evaluate.Distance.distance_meter import calculate_distance_manhattan
from .MatrixManage.ManageMatrix import min_values_sum

def evaluate(bus_stop_list):
    if not bus_stop_list:
        return 0

    min_values = min_values_sum(bus_stop_list=bus_stop_list)

    puntuation = 0.0

    for value in min_values:
        puntuation += value["value"]

    return puntuation