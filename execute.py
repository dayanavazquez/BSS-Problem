import random
import utils
# ----------------------------------------------------------------------
# Import the objective function and operator from the corresponding problem
# ----------------------------------------------------------------------

from Problem.BSSProblem import (
    print_solution_bss,
    present_problem, 
    objective_function, 
    random_solution, 
    not_random_solution, 
    random_change, 
    not_random_change, 
    random_permutation, 
    random_combination
)

# ----------------------------------------------------------------------
# General configuration of the search procedures: By default
# ----------------------------------------------------------------------

OBJECTIVE_MAX   = False       # goal of the optimization, True: maximization, False: minimization
MAX_TRIALS      = 1000       # maximum number of solutions to be explored by each metaheuristic
ECHO            = False      # printing some traces of the run
GENERATION_SIZE =  10        # number of generations, for P-metaheuristics
BEST_REFERENCES =   4        # number of solutions considered in the construction of the next generation, for P-metaheuristics
GENERATIONAL    =  False     # type of replacement in P-metaheuristics, True: generational, False: SteadyState
SYSTEMATIC_S_INI=  True      # Systematic search, True: From an arbitrary initial solution, False: from random solution
RUNS=1
TRESHOLD = 1  # For TA and RRT
CRITERION = 'TA'  # 'TA': Treshold accepting, 'RRT': Record-to-Record Travel

def set_default_parameters():
    global OBJECTIVE_MAX, MAX_TRIALS, ECHO, \
           GENERATION_SIZE, BEST_REFERENCES, \
           GENERATIONAL, SYSTEMATIC_S_INI, \
           TRESHOLD, CRITERION, \
           RUNS
    OBJECTIVE_MAX = False  # goal of the optimization, True: maximization, False: minimization
    MAX_TRIALS = 1000  # maximum number of solutions to be explored by each metaheuristic
    ECHO = False  # printing some traces of the run
    GENERATION_SIZE = 10  # number of generations, for P-metaheuristics
    BEST_REFERENCES = 4  # number of solutions considered in the construction of the next generation, for P-metaheuristics
    GENERATIONAL = False  # type of replacement in P-metaheuristics, True: generational, False: SteadyState
    SYSTEMATIC_S_INI = False  # Systematic search, True: From an arbitrary initial solution, False: from random solution
    TRESHOLD = 1 # For TA and RRT
    CRITERION = 'TA' # 'TA': Treshold accepting, 'RRT': Record-to-Record Travel
    RUNS = 1

def print_parameters(search_procedure = ''):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    if search_procedure == '':
        print(f'Default parameters for all search procedures')
    else:
        print(f'Parameters for {search_procedure}')
    print(f'OBJECTIVE_MAX = {OBJECTIVE_MAX}')
    print(f'MAX_TRIALS = {MAX_TRIALS}')
    print(f'ECHO = {ECHO}')
    if search_procedure in {'', 'mh_EvolutionStrategy', 'mh_GeneticAlgorithm'}:
        print(f'GENERATION_SIZE = {GENERATION_SIZE}')
        print(f'BEST_REFERENCES = {BEST_REFERENCES}')
        print(f'GENERATIONAL = {GENERATIONAL}')
    if search_procedure in {'', 'systematicSearch'}:
        print(f'SYSTEMATIC_S_INI = {SYSTEMATIC_S_INI}')
    if search_procedure in {'', 'mh_LocalSearch'}:
        print(f'CRITERION = {CRITERION}')
        print(f'TRESHOLD = {TRESHOLD}')
    print(f'RUNS = {RUNS}')

def set_parameters(custom_parameters):
    set_default_parameters()
    global OBJECTIVE_MAX, MAX_TRIALS, ECHO, \
           GENERATION_SIZE, BEST_REFERENCES, \
           GENERATIONAL, SYSTEMATIC_S_INI, \
           CRITERION, TRESHOLD, \
           RUNS
    for key, value in custom_parameters.items():
        if key =='OBJECTIVE_MAX':
            OBJECTIVE_MAX = value
        elif key == 'MAX_TRIALS':
            MAX_TRIALS = value
        elif key == 'ECHO':
            ECHO = value
        elif key == 'GENERATION_SIZE':
            GENERATION_SIZE = value
        elif key == 'BEST_REFERENCES':
            BEST_REFERENCES = value
        elif key == 'GENERATIONAL':
            GENERATIONAL = value
        elif key == 'SYSTEMATIC_S_INI':
            SYSTEMATIC_S_INI = value
        elif key == 'CRITERION':
            CRITERION = value
        elif key == 'TRESHOLD':
            TRESHOLD = value
        elif key == 'RUNS':
            RUNS = value
        else:
            print(f'Unknown parameter {key} = {value}')
    print()

# ----------------------------------------------------------------------
# ///////////////
# ----------------------------------------------------------------------

def print_solution(solution, description):
    print(f"{description}\n")
    print_solution_bss(solution, objective_function(solution))

def is_better_than(evaluation1,evaluation2):
    greater1 = (evaluation1>evaluation2)
    return (((evaluation1==evaluation2))or(OBJECTIVE_MAX)and greater1)or(not(OBJECTIVE_MAX)and not greater1)

def systematicSearch():
    if SYSTEMATIC_S_INI==True:
        best_solution = not_random_solution()
    else:
        best_solution = random_solution()
    best_evaluation = objective_function(best_solution)
    if ECHO:
        print(best_solution, best_evaluation)
    solution = best_solution.copy()
    for i in range(MAX_TRIALS-1):
        solution = not_random_change(solution)
        evaluation = objective_function(solution)
        if is_better_than(evaluation,best_evaluation):
            best_evaluation = evaluation
            best_solution = solution.copy()
        if ECHO:
            print(solution,evaluation,best_solution, best_evaluation)
    return best_solution

def mh_RandomSearch():
    best_solution = random_solution()
    best_evaluation = objective_function(best_solution)
    if ECHO:
        print(best_solution, best_evaluation)
    for i in range(MAX_TRIALS-1):
        solution = random_solution()
        evaluation = objective_function(solution)
        if ECHO:
            print(solution,evaluation)
        if is_better_than(evaluation,best_evaluation):
            best_evaluation= evaluation
            best_solution= solution
    return best_solution

def mh_HillClimbing():
    best_solution = random_solution()
    best_evaluation = objective_function(best_solution)
    if ECHO:
        print(best_solution, best_evaluation)
    for i in range(MAX_TRIALS):
        solution = random_change(best_solution.copy()) # a change with respect to the best solution
        evaluation = objective_function(solution)
        if ECHO:
            print(solution,evaluation)
        if is_better_than(evaluation, best_evaluation):
            best_evaluation= evaluation
            best_solution= solution
            if ECHO:
                print('change reference')
    return best_solution

def mh_RandomWalk():
    best_solution = random_solution()
    best_evaluation = objective_function(best_solution)
    if ECHO:
        print(best_solution, best_evaluation)
    last_solution= best_solution
    for i in range(MAX_TRIALS):
        solution = random_change(last_solution.copy()) # a change with respect to the last solution
        evaluation = objective_function(solution)
        if ECHO:
            print(solution,evaluation,last_solution)
        last_solution = solution
        if is_better_than(evaluation, best_evaluation):
            best_evaluation= evaluation
            best_solution= solution
    return best_solution

def need_to_change_reference(solution,ref_solution,best_solution):
    # for Local Search the decision to change the reference
    evalS = objective_function(solution)
    evalR = objective_function(ref_solution)
    evalB = objective_function(best_solution)
    need_to_change_reference = False
    if (CRITERION == 'TA') and \
       ( (    OBJECTIVE_MAX and evalS >= (evalR - TRESHOLD)) or
         (not OBJECTIVE_MAX and evalS <= (evalR + TRESHOLD)) ) :
        need_to_change_reference = True
    elif (CRITERION == 'RRT') and \
       ( (    OBJECTIVE_MAX and evalS >= (evalB - TRESHOLD)) or
         (not OBJECTIVE_MAX and evalS <= (evalB + TRESHOLD)) ) :
        need_to_change_reference = True
    return need_to_change_reference

def mh_LocalSearch(): # several LS algorithms (TA,RRT,HC), depending on the parameters
    best_solution = random_solution()
    best_evaluation = objective_function(best_solution)
    if ECHO:
        print(best_solution, best_evaluation)
    ref_solution= best_solution
    for i in range(MAX_TRIALS):
        solution = random_change(ref_solution.copy()) # a change with respect to the reference solution
        evaluation = objective_function(solution)
        if ECHO:
            print(solution,evaluation,ref_solution)
        if need_to_change_reference(solution,ref_solution,best_solution):
            ref_solution = solution
        if is_better_than(evaluation, best_evaluation):
            best_evaluation= evaluation
            best_solution= solution
    return best_solution

def insert_sorted(list,element,firstN): # the firstN are sorted acoording to is_better_than, element=[key,value]
    i=0
    while i<len(list) and i<firstN and is_better_than(list[i][0],element[0]):
        i+=1
    list.insert(i,element)
    return list

def mh_EvolutionStrategy():
    solutions=[]
    for i in range(GENERATION_SIZE):
        solution   = random_solution()
        evaluation = objective_function(solution)
        solutions  = insert_sorted(solutions, [evaluation,solution], BEST_REFERENCES)
    for g in range(1,int(MAX_TRIALS/GENERATION_SIZE)):
        if ECHO:
            print(f'generation:{g}')
        new_solutions=[]
        for i in range(GENERATION_SIZE):
            parent = random.randint(0, BEST_REFERENCES)
            # a change with respect to one of the best solutions
            solution = random_change(solutions[parent][1].copy())
            evaluation = objective_function(solution)
            new_solutions = insert_sorted(new_solutions, [evaluation, solution], BEST_REFERENCES)
        if ECHO:
            print(f'solutions    :{solutions}')
            print(f'new_solutions:{new_solutions}')
        if GENERATIONAL:
            solutions= new_solutions
        else:
            for i in range(BEST_REFERENCES):
                evaluation, solution = new_solutions[i][0], new_solutions[i][1]
                solutions = insert_sorted(solutions, [evaluation, solution], BEST_REFERENCES)
        if ECHO:
            print(f'solutions    :{solutions}')
            print()
    best_solution = solutions[0][1]
    return best_solution

def mh_GeneticAlgorithm():
    solutions = []
    for i in range(GENERATION_SIZE):
        solution   = random_solution()
        evaluation = objective_function(solution)
        solutions  = insert_sorted(solutions, [evaluation,solution], BEST_REFERENCES)
    for g in range(1,int(MAX_TRIALS/GENERATION_SIZE)):
        if ECHO:
            print(f'generation:{g}')
        new_solutions=[]
        for i in range(GENERATION_SIZE):
            parent1 = random.randint(0, BEST_REFERENCES)
            parent2 = random.randint(0, BEST_REFERENCES)
            # a combination of two of the best solutions
            solution = random_combination(solutions[parent1][1].copy(),solutions[parent2][1].copy())
            evaluation = objective_function(solution)
            new_solutions = insert_sorted(new_solutions, [evaluation, solution], BEST_REFERENCES)
        if ECHO:
            print(f'solutions    :{solutions}')
            print(f'new_solutions:{new_solutions}')
        if GENERATIONAL:
            solutions= new_solutions
        else:
            for i in range(BEST_REFERENCES):
                evaluation, solution = new_solutions[i][0], new_solutions[i][1]
                solutions = insert_sorted(solutions, [evaluation, solution], BEST_REFERENCES)
        if ECHO:
            print(f'solutions    :{solutions}')
            print()
    best_solution = solutions[0][1]
    return best_solution

def execute_mh(search_procedure, run = 0):
    if search_procedure in {
                'mh_RandomSearch', 'mh_RandomWalk',
                'mh_HillClimbing', 'mh_LocalSearch',
                'mh_EvolutionStrategy', 'mh_GeneticAlgorithm',
                'systematicSearch'}:
        if run == 0:
            print_parameters(search_procedure)
    if search_procedure == 'mh_RandomSearch':
        best = mh_RandomSearch()
    elif search_procedure == 'mh_RandomWalk':
        best = mh_RandomWalk()
    elif search_procedure == 'mh_HillClimbing':
        best = mh_HillClimbing()
    elif search_procedure == 'mh_LocalSearch':
        best = mh_LocalSearch()
    elif search_procedure == 'mh_EvolutionStrategy':
        best = mh_EvolutionStrategy()
    elif search_procedure == 'mh_GeneticAlgorithm':
        best = mh_GeneticAlgorithm()
    elif search_procedure == 'systematicSearch':
        best = systematicSearch()
    else:
        best = random_solution()
        print('Unknown search procedure')
    return best.copy()

def compare_search_procedures(search_procedures):
    present_problem()
    results = [[] for s in range(len(search_procedures))]
    for s in range(len(search_procedures)):
        search_procedure = search_procedures[s][0]
        parameters = search_procedures[s][1]
        set_parameters(parameters)
        for r in range(RUNS):
            solution = execute_mh(search_procedure, r)
            evaluation = objective_function(solution)
            if ((s == 0) and (r == 0)) or (is_better_than(evaluation,best_evaluation)):
                best = solution.copy()
                best_evaluation = evaluation
            results[s].append(evaluation)
            if ECHO:
                print_solution(solution, search_procedure+"run"+str(r))
        print(search_procedure,':',results[s])
    print()
    print_solution(best,'Best solution found ---> ')
    return(results)


def print_results(search_procedures,results_all):
    for s in range(len(search_procedures)):
        print(search_procedures[s][0],' (',search_procedures[s][1],') ',results_all[s])

SEARCH_PROCEDURES = [
['mh_HillClimbing', {'MAX_TRIALS': 1000, 'RUNS':5, 'TRESHOLD':3}],

# ['mh_LocalSearch',  {'MAX_TRIALS': 1000, 'RUNS':20, 'TRESHOLD':0, 'CRITERION':'TA'}],
# ['mh_LocalSearch',  {'MAX_TRIALS': 1000, 'RUNS':20, 'TRESHOLD':0, 'CRITERION':'RRT'}],
# ['mh_LocalSearch',  {'MAX_TRIALS': 1000, 'RUNS':20, 'TRESHOLD':10, 'CRITERION':'TA'}],
# ['mh_LocalSearch',  {'MAX_TRIALS': 1000, 'RUNS':20, 'TRESHOLD':10, 'CRITERION':'RRT'}],

# ['systematicSearch', {'MAX_TRIALS': 10000, 'RUNS':1}],
# ['systematicSearch', {'MAX_TRIALS': 234, 'RUNS': 10, 'SYSTEMATIC_S_INI': False}],
# ['systematicSearch', {'MAX_TRIALS': 234, 'RUNS': 1}],

# ['mh_RandomWalk', {'MAX_TRIALS': 1000}],
# ['mh_LocalSearch', {'MAX_TRIALS': 100}],

# ['mh_EvolutionStrategy', {'MAX_TRIALS': 1000, 'RUNS': 10,'GENERATION_SIZE':  100, 'BEST_REFERENCES':  50} ],
# ['mh_EvolutionStrategy', {'MAX_TRIALS': 1000}],
# ['mh_GeneticAlgorithm', {'MAX_TRIALS': 1000, 'GENERATION_SIZE':  100, 'BEST_REFERENCES':  50} ],
# ['mh_GeneticAlgorithm', {'MAX_TRIALS': 10000, 'RUNS': 10}]
]

# print_solution(random_solution(), "INITIAL SOLUTION")

print_parameters()
print()
results = compare_search_procedures(SEARCH_PROCEDURES)
print_results(SEARCH_PROCEDURES,results)
