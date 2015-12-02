#!/usr/bin/python

'''

TODO:
    Save visualizations along the way

'''

import os
import shutil
import sys
import pdb
import ga
import subprocess
import time
import numpy
from util import *

NUM_ISLANDS_DEFAULT_VALUE=8
NUM_INTER_ISLAND_COMBINATIONS=400

GENERATIONS_PER_ITERATION_DEFAULT_VALUE=25

def run_parallel_commands_silently(command_list):
    child_processes = []
    for command in command_list:
        child = subprocess.Popen(command,stdin=None,stdout=open(os.devnull, 'w'), shell=True)
        child_processes.append(child)
    for child in child_processes:
        child.wait()

def usage():
    print >> sys.stderr, 'Usage of '+__file__+' is the similar to that of ga.py. '+__file__+' has some additional options.'
    print >> sys.stderr, ''
    print >> sys.stderr, 'python '+__file__+' <options>'
    print >> sys.stderr, ''
    print >> sys.stderr, 'Options for '+__file__+':'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -num_islands <int>'
    print >> sys.stderr, '        Number of islands. Default value is '+str(NUM_ISLANDS_DEFAULT_VALUE)+'. Should ideally be the max number of threads your machine can run without any of the threads slowing each other down significantly.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -num_inter_island_combinations <int>'
    print >> sys.stderr, '        Number of times the populations of the islands are combined with each other to form new islands that are intiailly identical with the best results from all the islands. This happens deterministically after every island finishes running through the number of generations specified by \'-generations\'. See ga.py usage below. The total number of times that each island runs through the number of generations specified by \'-generations\' is num_inter_island_combinations. The first iteration\'s starting generation is seeded by starting_generation_descriptor_dir. Every other iteration\'s starting generation is seeded by the pareto frontier of the results of the previous iteration. The final result of this program is the pareto frontier of last combination of the islands.'
    print >> sys.stderr, ''
    print >> sys.stderr, 'The usage for ga.py is shown below.'
    print >> sys.stderr, ''
    ga.usage()

def main():
    os.system('clear') 
    
    start_time=time.time()
    
    if len(sys.argv) < 1 or '-usage' in sys.argv: 
        usage()
    
    population_size = int(get_command_line_param_val_default_value(sys.argv, '-population_size', ga.POPULATION_SIZE_DEFAULT_VALUE))
    generations = int(get_command_line_param_val_default_value(sys.argv, '-generations', GENERATIONS_PER_ITERATION_DEFAULT_VALUE))
    tournament_size = int(get_command_line_param_val_default_value(sys.argv, '-tournament_size', ga.TOURNAMENT_SIZE_DEFAULT_VALUE))
    elite_percent = float(get_command_line_param_val_default_value(sys.argv, '-elite_percent', ga.ELITE_PERCENT_DFAULT_VALUE))
    mate_percent = float(get_command_line_param_val_default_value(sys.argv, '-mate_percent', ga.MATE_PERCENT_DEFAULT_VALUE))
    mutation_percent = float(get_command_line_param_val_default_value(sys.argv, '-mutation_percent', ga.MUTATION_PERCENT_DEFAULT_VALUE))
    starting_generation_descriptor_dir0 = os.path.abspath(get_command_line_param_val_default_value(sys.argv, '-starting_generation_descriptor_dir', ga.STARTING_GENERATION_DESCRIPTOR_DIR_DEFAULT_VALUE))
    output_dir = os.path.abspath(get_command_line_param_val_default_value(sys.argv, '-output_dir', ga.OUTPUT_DIR_DEFAULT_VALUE))
    num_islands = int(get_command_line_param_val_default_value(sys.argv, '-num_islands', NUM_ISLANDS_DEFAULT_VALUE))
    num_inter_island_combinations = int(get_command_line_param_val_default_value(sys.argv, '-num_inter_island_combinations', NUM_INTER_ISLAND_COMBINATIONS))
    
    print "Island GA Parameters"
    print "    population_size:", population_size
    print "    generations:", generations
    print "    tournament_size:", tournament_size
    print "    elite_percent: %.2f%%" % elite_percent
    print "    mate_percent: %.2f%%" % mate_percent
    print "    mutation_percent: %.2f%%" % mutation_percent
    print "    starting_generation_descriptor_dir:", starting_generation_descriptor_dir0
    print "    num_islands:", num_islands
    print "    num_inter_island_combinations:", num_inter_island_combinations
    print "    output_dir:", output_dir
    print 
    
    sys.stdout = open(os.devnull, 'w') # Temporarily suppress output
    ga.initialize_guest_and_host_data(output_dir) # Make sure these host and guest variables are initialized so that the Genome.get_N_value() and Genome.get_P_value() methods work
    sys.stdout = sys.__stdout__ # Restore output
    fig, subplot = ga.get_subplots()
    temp_dir = join_paths([output_dir,'island_ga_temp'])
    makedirs(temp_dir)
    makedirs(join_paths([os.path.abspath(output_dir),'N_P_data_csv']))
    makedirs(join_paths([os.path.abspath(output_dir),'genome_data']))
    makedirs(join_paths([os.path.abspath(output_dir),'graphs']))
    makedirs(temp_dir)
    starting_generation_descriptor_dir=starting_generation_descriptor_dir0
    for island_processing_iteration in xrange(num_inter_island_combinations):
        print "Working on island iteration %d." % island_processing_iteration
        result_dirs_list = []
        command_list = []
        info_tuple = (population_size, generations, tournament_size, elite_percent, mate_percent, mutation_percent, starting_generation_descriptor_dir)
        for island_index in xrange(num_islands):
            island_output_dir_name = join_paths([temp_dir,'output_[iteration:'+str(island_processing_iteration)+'][island_index:'+str(island_index)+']'])
            makedirs(island_output_dir_name)
            result_dirs_list.append(island_output_dir_name)
            command = ('python ga.py -population_size %d -generations %d -tournament_size %d -elite_percent %f -mate_percent %f -mutation_percent %f -starting_generation_descriptor_dir %s -output_dir '+island_output_dir_name) % info_tuple
            command_list.append(command)
        run_parallel_commands_silently(command_list)
        iteration_output_dir = join_paths([temp_dir,'combined_results_[iteration:'+str(island_processing_iteration)+']'])
        makedirs(iteration_output_dir)
        for island_index,d in enumerate(result_dirs_list):
            shutil.copy(join_paths([d,'global_pareto_frontier.py']),join_paths([iteration_output_dir,'island_'+str(island_index)+'_global_pareto_frontier.py']))
        starting_generation_descriptor = iteration_output_dir
        # Save visualizations
        genomes=[]
        for file_name in list_dir_abs(starting_generation_descriptor):
            line = open(file_name,'r').readlines()[0].replace('Genome(','ga.Genome(')
            d = dict()
            exec line in globals(), d
            genomes+=d['genomes']
        # Get final pareto frontier
        genomes=[(genome, 1/(1.0+genome.get_N_value()), 1/(1.0+genome.get_P_value())) for genome in genomes]
        genomes=sorted(genomes, key=lambda x:(x[1],-x[2])) #sorted by lowest to highest inverse N, then by highest to lowest inverse P
        prev_inverse_P=inf
        indices_to_avoid=[]
        for i,(genome, inverse_N, inverse_P) in enumerate(genomes):
            if inverse_P<=prev_inverse_P:
                prev_inverse_P=inverse_P
                continue
            indices_to_avoid.append(i)
        for i in indices_to_avoid[::-1]:
            genomes.pop(i)
        with open(join_paths([os.path.abspath(output_dir),'genome_data','iteration_'+str(island_processing_iteration)+'.py']),'w') as f:
            f.write('genomes='+[e[0] for e in genomes].__repr__())
        genomes=[(e[0], 1/e[1]-1, 1/e[2]-1) for e in genomes]
        # Save visualization and data
        with open(join_paths([os.path.abspath(output_dir),'N_P_data_csv','iteration_'+str(island_processing_iteration)+'.csv']),'w') as f:
            f.write('N, P\n')
            for _,n,p in genomes:
                f.write(str(int(n))+', '+str(int(p))+'\n')
        subplot.set_title('Island GA Iteration '+str(island_processing_iteration))
        x = [int(e[1]) for e in genomes] # N values
        y = [int(e[2]) for e in genomes] # P values
        color=numpy.random.rand(3,1)
        subplot.plot(x, y, zorder=10, c=color, alpha=1.0)
        subplot.scatter(x, y, zorder=10, c=color, alpha=1.0)
        ga.add_upper_left_text_box(subplot, "Max N: (N:"+str(x[0])+",P:"+str(y[0])+")\nMax P: (N:"+str(x[-1])+",P:"+str(y[-1])+")")
        fig.savefig(join_paths([output_dir,'graphs','iteration_'+str(island_processing_iteration)+'.png']))
    fig.savefig(join_paths([output_dir,'graphs','final_result.png']))
    matplotlib.pyplot.close(fig)
    
    print 
    print 'Total Run Time: '+str(time.time()-start_time)
    print 

if __name__ == '__main__':
    main()

