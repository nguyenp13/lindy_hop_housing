#!/usr/bin/python

#POPULATION_SIZES=[25,50,100,200,400]
#TOURNAMENT_SIZES=[2,4,8,16,32]
#ELITE_MATE_MUTATION_PERCENT_COMBINATIONS=[
#    (30,35,35),
#    (50,25,25),
#    (70,15,15),
#    (90,05,05),
#]

POPULATION_SIZES=[25,100,400]
TOURNAMENT_SIZES=[2,4,8]
ELITE_MATE_MUTATION_PERCENT_COMBINATIONS=[
    (70,15,15),
    (90,05,05),
]

for (elite_percent, mate_percent, mutation_percent) in ELITE_MATE_MUTATION_PERCENT_COMBINATIONS:
    for tournament_size in TOURNAMENT_SIZES:
        for population_size in POPULATION_SIZES:
            info_tuple = (population_size, tournament_size, elite_percent, mate_percent, mutation_percent)
            output_dir_name = 'output_[population_size:%d][tournament_size:%d][elite_percent:%d][mate_percent:%d][mutation_percent:%d]' % info_tuple
            print ('python ga.py -population_size %d -generations 1000 -tournament_size %d -elite_percent %d -mate_percent %d -mutation_percent %d -output_dir '+output_dir_name) % info_tuple
