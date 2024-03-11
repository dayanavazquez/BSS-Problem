import random as ran, sys
from Problem.ManageProblem import generate_bus_stop

def generate_int(init: int = 1, end: int = 10):
    return ran.randint(init, end)

def generate_float(init: float = -20, end: float = 20):
    return ran.uniform(init, end)

def generate_probability():
    return generate_float(init=0, end=1)

def extract_bus_stop_coordinates(bus_stop_list):
    coordinates = []

    for bss in bus_stop_list:
        coordinates.append(
            bss.location.coordinate_x
        )

        coordinates.append(
            bss.location.coordinate_y
        )

    return coordinates

def reconstruct_bus_stop(coordinates_list):

    return [generate_bus_stop(
            coordinate_x=coordinates_list[i], 
            coordinate_y=coordinates_list[i + 1], 
            id=i
            ) for i in range(0, len(coordinates_list), 2)
    ]

BIG_FLOAT: float = sys.float_info.max

default = [
    -15.6, -6.2,
    -18.9, 13.5,
    -7.3, 9.8,
    8.2, 19.1,
    10.5, 2.3,
    -9.4, 11.8,
    -16.7, -3.6,
    7.9, -17.4,
    -5.1, -1.9,
    6.8, 16.7,
    -3.2, -14.8,
    -11.1, -5.5,
    19.8, -8.9,
    -1.6, -12.0,
    13.7, -18.2,
    2.4, 7.3,
    0.9, 4.1,
    -19.5, -10.3,
    -2.8, -2.1,
    15.4, -0.7
]
