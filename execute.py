from metaheuristics import multi_run, heuristic_solution, simple_mh_run

instances = [
    "instance_10",
    "instance_20",
    "instance_30",
    "instance_50",
    "instance_70",
    "instance_100",
    "instance_120",
    "instance_160",
    "instance_180", 
    "instance_200",
    "instance_250",
    "instance_300"
    ]

mh = [
    'mh_HillClimbing',
    'mh_EvolutionStrategy',
    'mh_RandomSearch'
]

conf_hc = [
    {'MAX_TRIALS': 2000, 'RUNS':10, 'TRESHOLD': 1.55},
    {'MAX_TRIALS': 1000, 'RUNS':10, 'TRESHOLD': 2.55},
    {'MAX_TRIALS': 1000, 'RUNS':10, 'TRESHOLD': 2.75},
    {'MAX_TRIALS': 1000, 'RUNS':10, 'TRESHOLD': 3.05},
    {'MAX_TRIALS': 1000, 'RUNS':10, 'TRESHOLD': 3.25}
]

conf_ee = [
    {'MAX_TRIALS': 1000, 'RUNS': 10,'GENERATION_SIZE': 60, 'BEST_REFERENCES': 30},
    {'MAX_TRIALS': 1000, 'RUNS': 10,'GENERATION_SIZE': 80, 'BEST_REFERENCES': 35},
    {'MAX_TRIALS': 1000, 'RUNS': 10,'GENERATION_SIZE': 120, 'BEST_REFERENCES': 60},
    {'MAX_TRIALS': 1000, 'RUNS': 10,'GENERATION_SIZE': 150, 'BEST_REFERENCES': 70},
    {'MAX_TRIALS': 1000, 'RUNS': 10}
]

conf_rs =[
    {'MAX_TRIALS': 1000, 'RUNS': 10},
    {'MAX_TRIALS': 1000, 'RUNS': 10},
    {'MAX_TRIALS': 1000, 'RUNS': 10},
    {'MAX_TRIALS': 1000, 'RUNS': 10},
    {'MAX_TRIALS': 1000, 'RUNS': 10}
]

# multi_run( 
#     instances=instances, 
#     mh=mh, 
#     conf_hc=conf_hc, 
#     conf_ee=conf_ee, 
#     conf_rs=conf_rs
# )

simple_mh_run(
    instance="instance_300", 
    mh="mh_HillClimbing", 
    conf={'MAX_TRIALS': 3000, 'RUNS':20, 'TRESHOLD': 9.75}
)

# heuristic_solution(instance="instance_300")