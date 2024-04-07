import random
import math

from Problem.ManageProblem import Point, BusStop, generate_bus_stop
from utils import (
    generate_probability, 
    generate_float, 
    generate_int, 
    extract_bus_stop_coordinates, 
    reconstruct_bus_stop, default
)

# ----------------------------------------------------------------------
# initializers
# ----------------------------------------------------------------------

def random_list(LIST_LENGTH=5, MIN_VALUE=-20.0, MAX_VALUE=20.0):
    lista = [0] * LIST_LENGTH
    for i in range(LIST_LENGTH):
        lista[i] = generate_bus_stop(
            coordinate_x=generate_float(init=MIN_VALUE, end=MAX_VALUE), 
            coordinate_y=generate_float(init=MIN_VALUE, end=MAX_VALUE),
            id=i
        )

    return lista

def random_permutation(LIST_LENGTH=5):
    a = [ default[i] for i in range(LIST_LENGTH)]
    b = [0] * LIST_LENGTH
    for i in range(LIST_LENGTH):
        pos = random.randint(0, len(a)-1)
        b[i] = a[pos]
        a.remove(b[i])

    print([
            generate_bus_stop(coordinate_x=b[i], coordinate_y=b[i + 1]) for i in range(len(b))
        ])

    return reconstruct_bus_stop(b)

# ----------------------------------------------------------------------
# operators
# ----------------------------------------------------------------------

def change1(solution, MIN_VALUE=-20, MAX_VALUE=20): # the value of a random position is randomly changed
    
    extract_solution = extract_bus_stop_coordinates(bus_stop_list=solution)
    
    l = len(extract_solution)

    pos1 = generate_int(init=0, end=l-1)
    extract_solution[pos1] = extract_solution[generate_int(init=0, end=l-1)]
    
    return reconstruct_bus_stop(coordinates_list=extract_solution)

def add1(solution, MIN_VALUE=-20, MAX_VALUE=20, displace=1): # the value of a position is randomly change +-1
    
    extract_solution = extract_bus_stop_coordinates(bus_stop_list=solution)

    l = len(extract_solution)
    pos1 = generate_int(init=0, end=l-1)

    if extract_solution[pos1] == MIN_VALUE:
        extract_solution[pos1] += displace

    elif extract_solution[pos1] == MAX_VALUE:
        extract_solution[pos1] -= displace

    else:
        if generate_probability() >= 0.5:
            extract_solution[pos1] += displace
        else:
            extract_solution[pos1] -= displace

    return reconstruct_bus_stop(coordinates_list=extract_solution)

def add1all(solution, MIN_VALUE=0, MAX_VALUE=10, displace=1): # the value of all positions is randomly change +-1
    
    extract_solution = extract_bus_stop_coordinates(bus_stop_list=solution)
    
    l = len(extract_solution)

    for pos1 in range(l):

        if extract_solution[pos1] == MIN_VALUE:
            extract_solution[pos1] += displace

        elif extract_solution[pos1] == MAX_VALUE:
            extract_solution[pos1] -= displace

        else:
            if generate_probability():
                extract_solution[pos1] += displace
            else:
                extract_solution[pos1] -= displace

    return reconstruct_bus_stop(coordinates_list=extract_solution)

def random_change_for_lists(solution, MIN_VALUE=-20, MAX_VALUE=20, displace=1):
    
    r = generate_probability()

    if r>= 0.66:
        # print('change1')
        solution =  change1(solution, MIN_VALUE, MAX_VALUE)
    elif r>= 0.33:
        # print('add1')
        solution = add1(solution, MIN_VALUE, MAX_VALUE, displace=displace)
    else:
        # print('add1all')
        solution = add1all(solution, MIN_VALUE, MAX_VALUE, displace=displace)

    return solution

'''
MIN_VALUE = 0
MAX_VALUE = 10
LIST_LENGTH = 4
INTEGER = False
sol =  random_list(LIST_LENGTH,MIN_VALUE,MAX_VALUE,INTEGER)
for i in range(10):
    #print(2*(random.random()-0.5))
    print(sol)
    sol = random_change_for_lists(sol,MIN_VALUE,MAX_VALUE,INTEGER)
'''

def interchange(solution): # the values in two positions is interchanged
    
    extract_solution = extract_bus_stop_coordinates(bus_stop_list=solution)

    l = len(extract_solution)

    pos1 = generate_int(init=0, end=l-1)
    pos2 = generate_int(init=0, end=l-1)

    pass_solution = extract_solution[pos1]

    extract_solution[pos1] = extract_solution[pos2]

    extract_solution[pos2] = pass_solution

    return reconstruct_bus_stop(coordinates_list=extract_solution)

def uniform_crossover(solution, solutionAlt): # each value is chosen randomly from any of the solutions
    
    extract_solution = extract_bus_stop_coordinates(bus_stop_list=solution)
    extract_solution_alt = extract_bus_stop_coordinates(bus_stop_list=solutionAlt)
    
    l = len(extract_solution)

    for i in range(l):
        if random.randint(0, l):
            extract_solution[i] = extract_solution_alt[i]

    return reconstruct_bus_stop(coordinates_list=extract_solution)

def ox_crossover(solution, solutionAlt): # OX crossover for permutation. A random section from one solution and the order values from the other solution
    size = len(solution)
    start, end = sorted([random.randint(0, size - 1) for _ in range(2)])
    new_solution = [-1] * size
    new_solution[start:end + 1] = solution[start:end + 1]
    to_add=[]
    for gene in solutionAlt: # get the values in solutionAlt not yet in new_solution
        if gene not in new_solution:
            to_add.append(gene)
    pos_to_add=0
    for i, v in enumerate(new_solution):
        if v == -1:
            new_solution[i] = to_add[pos_to_add]
            pos_to_add+=1
    return new_solution


def mixed_crossover(solution1, solution2):
    p = generate_probability()

    solution = None

    if p < 0.5:
        solution = ox_crossover(solution=solution1, solutionAlt=solution2)
    elif p >= 0.5:
        solution = uniform_crossover(solution=solution1, solutionAlt=solution2)

    if generate_probability() <= 0.2:
        solution = random_change_for_lists(solution=solution)

    return solution

# ----------------------------------------------------------------------
# for exhaustive search
# ----------------------------------------------------------------------

def first_list(LIST_LENGTH=10, MIN_VALUE=0, MAX_VALUE=10):
    number= LIST_LENGTH
    solution= [MIN_VALUE for i in range(number)]
    return solution

def next_list(solution,LIST_LENGTH=10, MIN_VALUE=0, MAX_VALUE=10, INTEGER=True, resolution=10):
    # resolution : steps between MIN_VALUE and MAX_VALUE
    number = LIST_LENGTH
    j= number-1
    while (solution[j]==MAX_VALUE) and j>=0:
        j-=1
    if j==-1:
        solution = first_list(number)
    else:
        if INTEGER:
            solution[j]+=1
            for j in range(j+1,number):
                solution[j]=MIN_VALUE
        else: # imposible exhaustive searh with infinite not integer... an approximation with steps
            step = (MAX_VALUE-MIN_VALUE)/ resolution
            solution[j]+=step
            if solution[j]>MAX_VALUE:
                solution[j] = MAX_VALUE
            for j in range(j+1,number):
                solution[j]=MIN_VALUE
    return solution

def first_permutation(LIST_LENGTH=5):
    number= LIST_LENGTH
    solution = [ default[i] for i in range(number)]

    return reconstruct_bus_stop(solution)

def next_permutation(solution, LIST_LENGTH=5):

    extract_solution = extract_bus_stop_coordinates(bus_stop_list=solution)

    number= LIST_LENGTH
    # go backward to find the first value that is smaller than the next (pair of consecutive values in ascending order)
    # take the elements after this value and sort them
    # place the first of these element that is greater than the value and place it in the position of the value
    # put the rest of these elements and the value after this position, in ascending order
    end_list=[]
    j= number-1
    end_list.append(extract_solution[j])
    while (extract_solution[j-1]>=extract_solution[j])and(j>0):
        j-=1
        end_list.append(extract_solution[j])
    if j==0:
        extract_solution = extract_bus_stop_coordinates( first_permutation(number) )
    else:
        end_list.sort()
        k=0
        while extract_solution[j-1] >= end_list[k]:
            k += 1
        tmp = extract_solution[j-1]
        extract_solution[j-1] = end_list[k]
        end_list[k] = tmp
        shft = j
        for i in range(j,number):
            extract_solution[i]=end_list[i-shft]
    return reconstruct_bus_stop(coordinates_list=extract_solution)