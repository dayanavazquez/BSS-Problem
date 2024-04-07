import json
import datetime

from utils import play_sound_finish

from .ManageProblem import Passenger, Point

def load_problem(instance):
    with open('Instances\instances.json', 'r') as load:
        problem = json.load(load)[instance]

        return {
            "max_distance_walk": problem["max_distance_walk"],
            "max_bus_stop": problem["max_bus_stop"],
            "max_coordinate": problem["max_coordinate"],
            "min_coordinate": problem["min_coordinate"],
            "passengers": [ 
                    Passenger(
                        location=Point(coordinate_x=p["coordinate_x"], coordinate_y=p["coordinate_y"]),
                        id=p["id"]
                    ) 
                    for p in problem["passengers"]
                ]
        }
        
def save_solution(data, instance, conf=None):

    problem = {}
    best = {"results": []}

    try:
        with open('Instances\saved_bss_best_results.json', 'r') as file:
            problem = json.load(file)
    except FileNotFoundError:
        problem = {"results": []}

    problem["results"].append(data["results"])

    with open('Instances\saved_bss_best_results.json', 'w') as file:
        json.dump(problem, file, indent=4)

    best_evers = {}

    best_ever = {
        "date_found": datetime.date.today(),
        "results": ""
    }

    new_best = {
        "date_found": datetime.date.today(),
        "results": ""
    }

    try:
        with open('Instances\Best_solution_ever.json', 'r') as file:
            best_evers = json.load(file)

            for b in best_evers["best_evers"]:
                if b["results"]["instance"] == instance:
                    best_ever = b
                    break

    except FileNotFoundError:
        best_evers = {"best_evers": []}

    changed_best = found_best_solution(problem=problem, best_solution=best_ever, instance=instance)
    
    with open('Instances\Best_solution_ever.json', 'w') as file:
        json.dump(best_evers, file, indent=4)

    play_sound_finish()
 
def found_best_solution(problem, best_solution, instance):

    for solution in problem["results"]:

        if "value" not in best_solution["results"]:
            best_solution["results"] = solution
            
        elif (not best_solution or solution["value"] < best_solution["results"]["value"]) and solution["instance"] == instance:   
            best_solution["results"] = solution
           
    best_solution["date_found"] = str(datetime.date.today())

    return best_solution
