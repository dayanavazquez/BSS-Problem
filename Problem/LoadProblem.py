import json

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
        
def save_solution(data):

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

    # with open('Instances\Best_solution_ever.json', 'w') as file:
    #     best = json.load(file)

    #     for b in problem["results"]:
    #         if b.value > best[ data["instance"] ].value:
    #             best = b

    #     json.dump(best, file, indent=4)
        

            