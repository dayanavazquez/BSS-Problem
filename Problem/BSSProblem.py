import json

import pyttsx3

import numpy as np, math
from .ManageProblem import BSS
from .LoadProblem import load_problem as l, save_solution
from Evaluate.evaluate_solution import evaluate, min_values_sum
from Operators.operators import (
    random_change_for_lists, 
    random_permutation, 
    random_list, 
    first_permutation, 
    interchange, 
    next_permutation, 
    mixed_crossover
)

MH = {
    "mh_HillClimbing": "escalador de colinas",
    "mh_EvolutionStrategy": "estrategia evolutiva",
    "mh_RandomSearch": "busqueda aleatoria"
}



bss: BSS = BSS()

presentation  = 'Bus Stop Selection problem Variant VRP'

def load_problem(instance, mh):
    data = l(instance=instance)

    bss.INSTANCE_PROBLEM = instance
    bss.PASSENGER_LIST = data["passengers"]
    bss.DISPLACE = 2.0
    bss.MAX_DISTANCE_WALK = data["max_distance_walk"]
    bss.MAX_BUS_STOP = data["max_bus_stop"]
    bss.MAX_COORDINATE = data["max_coordinate"]
    bss.MIN_COORDINATE = data["min_coordinate"]
    bss.METAHEURISTIC = mh

def present_problem():
    print('----------------------------------------------------------------------\n')
    print(presentation)
    print("\n")
    print(f"MAX PASSENGERS: {len(bss.PASSENGER_LIST)}")
    print(f"MAX BUS STOP: {bss.MAX_BUS_STOP}\n")
    print('----------------------------------------------------------------------')


def objective_function(solution):
    return evaluate(bus_stop_list=solution, passenger_list=bss.PASSENGER_LIST)

def random_solution():
    return random_list(LIST_LENGTH=bss.MAX_BUS_STOP)

def not_random_solution():
    return first_permutation(LIST_LENGTH=bss.MAX_BUS_STOP)

def random_change(solution):
    return random_change_for_lists(
        solution=solution, 
        MIN_VALUE=bss.MIN_COORDINATE, 
        MAX_VALUE=bss.MAX_COORDINATE, 
        displace=bss.DISPLACE
    )

def not_random_change(solution):
    return next_permutation(solution=solution,LIST_LENGTH=bss.MAX_BUS_STOP)

def random_combination(solution1,solution2):
    return mixed_crossover(solution1,solution2)

def print_solution_bss(mh: str, bus_stop_list, eval, conf=None):
    
    bus_stop_list = assign_passengers(bus_stop_list=bus_stop_list)

    save_bus_stop(mh=mh, bus_stop_list=bus_stop_list, eval=eval, conf=conf)

    tam = bss.INSTANCE_PROBLEM[9:]

    translate = f'Mejor evaluación encontrada con la metaheuristica {MH[mh]}: {eval}, Instancia del problema: {tam}'

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    print("**********************************************************\n")

    print(f"Best solution eval: {eval}")
    print(f"Used MH: {mh}")
    print(f"Total number of bus stop: {len(bus_stop_list)} ")

    for bus_stop in bus_stop_list:
        print(str(bus_stop))
    
    print("\n")
    print("**********************************************************\n")

    engine = pyttsx3.init()
    engine.setProperty('rate', 143)
    engine.say(translate)
    engine.runAndWait()


def assign_passengers(bus_stop_list):

    min_values = min_values_sum(bus_stop_list=bus_stop_list, passenger_list=bss.PASSENGER_LIST)

    for value in min_values:
        bus_stop_list[ value["column"] ].passenger_list.append(bss.PASSENGER_LIST[ value["row"] ].id)

    return bus_stop_list

def save_bus_stop(mh: str, bus_stop_list, eval, conf=None):
    bus_stop = []

    for bus in bus_stop_list:
        info = {"bus_stop_info": str(bus)}

        bus_stop.append(info)

    data = {
        "results": {
            "instance": bss.INSTANCE_PROBLEM,
            "METAHEURISTIC": mh,
            "value": eval,
            "MAX_BUS_STOP": bss.MAX_BUS_STOP,
            "MAX_DISTANCE_WALK": bss.MAX_DISTANCE_WALK,
            "max_passengers": len(bss.PASSENGER_LIST),
            "conf": conf,
            "bus_stops": bus_stop
        }
    }

    save_solution(data, instance=bss.INSTANCE_PROBLEM)

    
    