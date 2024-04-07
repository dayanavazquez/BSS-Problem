import numpy as np, math

from ..Distance.distance_meter import calculate_distance_manhattan
from utils import  BIG_FLOAT

def _generate_matrix(bus_stop_list, passenger_list):

    cost_matrix = []

    for passenger in passenger_list:
        distances = []
        
        for bus_stop in bus_stop_list:

            distances.append(
                calculate_distance_manhattan(
                    init_point=passenger.location,
                    end_point=bus_stop.location
                )
            )

        cost_matrix.append(distances)

    return np.array(cost_matrix)

def min_values_sum(bus_stop_list, passenger_list):

    result = []

    cost_matrix = _generate_matrix(bus_stop_list=bus_stop_list, passenger_list=passenger_list)

    while True:

        row, column = np.unravel_index(np.argmin(cost_matrix), cost_matrix.shape)

        result.append(
            {
                "row": row,
                "column": column,
                "value": cost_matrix[row, column]
            }
        )

        cost_matrix[row, :] = BIG_FLOAT

        if np.all(cost_matrix == BIG_FLOAT):
            break

    return result