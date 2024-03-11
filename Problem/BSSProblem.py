import json
import numpy as np, math
from .LoadProblem import load_problem, save_solution
from Evaluate.evaluate_solution import evaluate, min_values_sum
from Operators.operators import (
    random_change_for_lists, 
    random_permutation, 
    random_list, 
    first_permutation, 
    interchange, 
    next_permutation, 
    uniform_crossover
)

INSTANCE_PROBLEM = "instance_27"

data = load_problem(instance=INSTANCE_PROBLEM)

passenger_list = data["passengers"]

MAX_DISTANCE_WALK = data["max_distance_walk"]
MAX_BUS_STOP = data["max_bus_stop"]

MAX_COORDINATE = data["max_coordinate"]
MIN_COORDINATE = data["min_coordinate"]

METAHEURISTIC = "mh_HillClimbing"

presentation  = 'Bus Stop Selection problem Variant VRP'

def present_problem():
    print('----------------------------------------------------------------------\n')
    print(presentation)
    print("\n")
    print(f"MAX PASSENGERS: {len(passenger_list)}")
    print(f"MAX BUS STOP: {MAX_BUS_STOP}\n")
    print('----------------------------------------------------------------------')


def objective_function(solution):
    return evaluate(bus_stop_list=solution)

def random_solution():
    return random_list(LIST_LENGTH=MAX_BUS_STOP)

def not_random_solution():
    return first_permutation(LIST_LENGTH=MAX_BUS_STOP)

def random_change(solution):
    # return interchange(solution=solution)
    return random_change_for_lists(
        solution=solution, 
        MIN_VALUE=-20.0, 
        MAX_VALUE=20.0, 
        displace=1
    )

def not_random_change(solution):
    return next_permutation(solution=solution,LIST_LENGTH=MAX_BUS_STOP)

def random_combination(solution1,solution2):
    return uniform_crossover(solution1,solution2)

def print_solution_bss(bus_stop_list, eval):
    
    bus_stop_list = assign_passengers(bus_stop_list=bus_stop_list)

    save_bus_stop(bus_stop_list=bus_stop_list, eval=eval)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    print("**********************************************************\n")

    print(f"Best solution eval: {eval}")
    print(f"Total number of bus stop: {len(bus_stop_list)} ")

    for bus_stop in bus_stop_list:

        print(str(bus_stop))

        print("Passengers assigned: ")
        bus_stop.inspect_passengers_assigned()
    
    print("\n")
    print("**********************************************************\n")


def assign_passengers(bus_stop_list):

    min_values = min_values_sum(bus_stop_list=bus_stop_list)

    for value in min_values:
        bus_stop_list[ value["column"] ].passenger_list.append(passenger_list[ value["row"] ].id)

    return bus_stop_list

def save_bus_stop(bus_stop_list, eval):
    bus_stop = []

    for bus in bus_stop_list:
        info = {"bus_stop_info": str(bus)}

        # passengers = []

        # for passenger in bus.passenger_list:
        #     passengers.append(
        #         {"passenger_info": str(passenger)}
        #     )

        # info["passengers"] = passengers

        bus_stop.append(info)


    data = {
        "results": {
            "instance": INSTANCE_PROBLEM,
            "metaheuristic": METAHEURISTIC,
            "value": eval,
            "max_bus_stop": MAX_BUS_STOP,
            "max_distance_walk": MAX_DISTANCE_WALK,
            "max_passengers": len(passenger_list),
            "bus_stops": bus_stop
        }
    }

    save_solution(data)
    