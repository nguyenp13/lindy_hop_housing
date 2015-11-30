#!/usr/bin/python

'''
TODO:
    Very Important
    
    Less Important
        Add parsing of actual data to add real hosts and guests instead of using the dummy func
        Refactor code so that we can run ga.py in parallel and have the results combined with a main.py
        Refactor each section of the main GA code into functions
        Get late night tendencies to be taken into account for the P value determinations1 
'''

import os
import sys
import pdb
import networkx
import time
import random
import copy
import numpy
import matplotlib
import matplotlib.pyplot
from util import *

SAVE_VISUALIZATIONS = True

DEFAULT_NUM_DUMMY_HOSTS = 100
DEFAULT_NUM_DUMMY_GUESTS = 100

POPULATION_SIZE_DEFAULT_VALUE = 25
GENERATIONS_DEFAULT_VALUE = 50
TOURNAMENT_SIZE_DEFAULT_VALUE = 8
ELITE_PERCENT_DFAULT_VALUE = 50
MATE_PERCENT_DEFAULT_VALUE = 30
MUTATION_PERCENT_DEFAULT_VALUE = 20
OUTPUT_DIR_DEFAULT_VALUE = './output'

housing_graph = None
hosts = [] 
guests = []

class Host(object):
    def __init__(self, name0='NO_NAME', email0='NO_EMAIL', phone_number0='', days_housing_is_available0=frozenset(['Friday', 'Saturday', 'Sunday']), has_cats0=False, has_dogs0=False, willing_to_house_smokers0=True, willing_to_provide_rides0=True, late_night_tendencies0="survivors' club", preferred_house_guests0=[], misc_info0='', id_num0=-1):
        self.name=name0
        self.email=email0
        self.phone_number=phone_number0 # is a string
        self.days_housing_is_available=days_housing_is_available0 # is a frozenset
        self.has_cats=has_cats0
        self.has_dogs=has_dogs0
        self.willing_to_house_smokers=willing_to_house_smokers0
        self.willing_to_provide_rides=willing_to_provide_rides0
        self.late_night_tendencies=late_night_tendencies0 # is a string
        self.preferred_house_guests=preferred_house_guests0
        self.misc_info=misc_info0 # is a string
        self.id_num=id_num0 
        assertion(len(self.days_housing_is_available)>0, 'Hosts must have at least one day of housing available.')
    
    def __str__(self):
        ans = '''
Host:
    ID Number: '''+str(self.id_num)+'''
    Name: '''+self.name+'''
    Email: '''+self.email+'''
    Phone Number: '''+self.phone_number+'''
    Days Housing Is Available: '''+(('Friday, ' if 'Friday' in self.days_housing_is_available else '')+('Saturday, ' if 'Saturday' in self.days_housing_is_available else '')+('Sunday, ' if 'Sunday' in self.days_housing_is_available else ''))[:-2]+'''
    Has Cats: '''+('Yes' if self.has_cats else 'No')+'''
    Has Dogs: '''+('Yes' if self.has_dogs else 'No')+'''
    Willing to House Smokers: '''+('Yes' if self.willing_to_house_smokers else 'No')+''' 
    Willing to Provide Rides: '''+('Yes' if self.willing_to_provide_rides else 'No')+'''
    Late Night Tendencies: '''+self.late_night_tendencies+'''
    Preferred House Guests: '''+', '.join(sorted(list(set([guest.name for guest in guests if guest.id_num in self.preferred_house_guests]))))+'''
    Misc. Info.: '''+self.misc_info+'''
'''
        return ans
    
    def __repr__(self):
        ans = ''+ \
            '''Host('''+ \
                '''name0='''+self.name.__repr__()+''', '''+ \
                '''email0='''+self.email.__repr__()+''', '''+ \
                '''phone_number0='''+self.phone_number.__repr__()+''', '''+ \
                '''days_housing_is_available0='''+self.days_housing_is_available.__repr__()+''', '''+ \
                '''has_cats0='''+self.has_cats.__repr__()+''', '''+ \
                '''has_dogs0='''+self.has_dogs.__repr__()+''', '''+ \
                '''willing_to_house_smokers0='''+self.willing_to_house_smokers.__repr__()+''', '''+ \
                '''willing_to_provide_rides0='''+self.willing_to_provide_rides.__repr__()+''', '''+ \
                '''late_night_tendencies0='''+self.late_night_tendencies.__repr__()+''', '''+ \
                '''preferred_house_guests0='''+self.preferred_house_guests.__repr__()+''', '''+ \
                '''misc_info0='''+self.misc_info.__repr__()+''', '''+ \
                '''id_num0='''+self.id_num.__repr__()+ \
            ''')'''
        return ans

class Guest(object):
    def __init__(self, name0='NO_NAME', email0='NO_EMAIL', phone_number0='', days_housing_is_needed0=frozenset(['Friday', 'Saturday', 'Sunday']), can_be_around_cats0=True, can_be_around_dogs0=True, smokes0=False, has_ride0=True, late_night_tendencies0="survivors' club", preferred_house_guests0=[], misc_info0='', id_num0=-1):
        self.name=name0
        self.email=email0
        self.phone_number=phone_number0 # is a string
        self.days_housing_is_needed=days_housing_is_needed0 # is a frozenset
        self.can_be_around_cats=can_be_around_cats0
        self.can_be_around_dogs=can_be_around_dogs0
        self.smokes=smokes0
        self.has_ride=has_ride0
        self.late_night_tendencies=late_night_tendencies0 # is a string
        self.preferred_house_guests=preferred_house_guests0
        self.misc_info=misc_info0 # is a string
        self.id_num=id_num0 
        assertion(len(self.days_housing_is_needed)>0, 'Guests must require at least one day of needed housing.')
    
    def __str__(self):
        ans = '''
Guest:
    ID Number: '''+str(self.id_num)+'''
    Name: '''+self.name+'''
    Email: '''+self.email+'''
    Phone Number: '''+self.phone_number+'''
    Days Housing Is Needed: '''+(('Friday, ' if 'Friday' in self.days_housing_is_needed else '')+('Saturday, ' if 'Saturday' in self.days_housing_is_needed else '')+('Sunday, ' if 'Sunday' in self.days_housing_is_needed else ''))[:-2]+'''
    Allergic to Cats: '''+('Yes' if not self.can_be_around_cats else 'No')+'''
    Allergic to Dogs: '''+('Yes' if not self.can_be_around_dogs else 'No')+'''
    Smokes: '''+('Yes' if self.smokes else 'No')+''' 
    Needs Transportation: '''+('Yes' if not self.has_ride else 'No')+'''
    Late Night Tendencies: '''+self.late_night_tendencies+'''
    Preferred Hosts: '''+', '.join(sorted(list(set([host.name for host in hosts if host.id_num in self.preferred_house_guests]))))+'''
    Preferred Fellow House Guests: '''+', '.join(sorted(list(set([guest.name for guest in guests if guest.id_num != self.id_num and guest.id_num in self.preferred_house_guests]))))+'''
    Misc. Info.: '''+self.misc_info+'''
'''
        return ans
    
    def __repr__(self):
        ans = ''+ \
            '''Guest('''+ \
                '''name0='''+self.name.__repr__()+''', '''+ \
                '''email0='''+self.email.__repr__()+''', '''+ \
                '''phone_number0='''+self.phone_number.__repr__()+''', '''+ \
                '''days_housing_is_needed0='''+self.days_housing_is_needed.__repr__()+''', '''+ \
                '''can_be_around_cats0='''+self.can_be_around_cats.__repr__()+''', '''+ \
                '''can_be_around_dogs0='''+self.can_be_around_dogs.__repr__()+''', '''+ \
                '''smokes0='''+self.smokes.__repr__()+''', '''+ \
                '''has_ride0='''+self.has_ride.__repr__()+''', '''+ \
                '''late_night_tendencies0='''+self.late_night_tendencies.__repr__()+''', '''+ \
                '''preferred_house_guests0='''+self.preferred_house_guests.__repr__()+''', '''+ \
                '''misc_info0='''+self.misc_info.__repr__()+''', '''+ \
                '''id_num0='''+self.id_num.__repr__()+ \
            ''')'''
        return ans

def are_compatible(host, guest):
    # Check if the days housing is needed is a subset of days housing is available
    if not guest.days_housing_is_needed.issubset(host.days_housing_is_available): 
        return False
    
    # Cat compatibility
    if not guest.can_be_around_cats: 
        if host.has_cats:
            return False
    
    # Dog compatibility
    if not guest.can_be_around_dogs: 
        if host.has_dogs:
            return False
    
    # Smoking compatibility
    if guest.smokes:
        if not host.willing_to_house_smokers:
            return False
    
    # Rides
    if not guest.has_ride:
        if not host.willing_to_provide_rides:
            return False
    
    return True

def same_person(h1,h2):
    # Each Host object actually represents a spot in a particular person's house, not that person. 
    # This function tells us if two Host objects represent the same person.
    return \
            h1.name==h2.name and \
            h1.email==h2.email and \
            h1.phone_number==h2.phone_number and \
            h1.days_housing_is_available==h2.days_housing_is_available and \
            h1.has_cats==h2.has_cats and \
            h1.has_dogs==h2.has_dogs and \
            h1.willing_to_house_smokers==h2.willing_to_house_smokers and \
            h1.willing_to_provide_rides==h2.willing_to_provide_rides and \
            h1.late_night_tendencies==h2.late_night_tendencies and \
            h1.preferred_house_guests==h2.preferred_house_guests and \
            h1.misc_info==h2.misc_info 

def generate_dummy_hosts_and_guests(num_hosts=DEFAULT_NUM_DUMMY_HOSTS, num_guests=DEFAULT_NUM_DUMMY_GUESTS):
    if os.path.isfile('test_data.py'):
         with open('test_data.py','r') as f:
            host_line, guest_line = f.readlines()
            exec host_line
            exec guest_line
            return hosts, guests
    host_ids = range(num_hosts)
    guest_ids = range(num_hosts, num_hosts+num_guests)
    num_preferred_house_guests=int(DEFAULT_NUM_DUMMY_HOSTS*0.3)
    
    hosts = [Host(
                name0='Dummy Host '+str(i), 
                has_cats0=random.choice([True,False]),
                has_dogs0=random.choice([True,False]),
                willing_to_house_smokers0=random.choice([True,False]),
                willing_to_provide_rides0=random.choice([True,False]),
                preferred_house_guests0=list(set(random.sample(guest_ids,num_preferred_house_guests))),
                id_num0=i,
            ) for i in host_ids]
    guests = [Guest(
                name0='Dummy Guest '+str(i), 
                can_be_around_cats0=random.choice([True,False]),
                can_be_around_dogs0=random.choice([True,False]),
                smokes0=random.choice([True,False]),
                has_ride0=random.choice([True,False]),
                preferred_house_guests0=list(set(random.sample(guest_ids,num_preferred_house_guests)+random.sample(host_ids,num_preferred_house_guests))), 
                id_num0=i,
            ) for i in guest_ids]
    with open('test_data.py','w') as f:
        f.write('hosts='+hosts.__repr__())
        f.write('\n')
        f.write('guests='+guests.__repr__())
    return hosts, guests

class Genome(object):
    
    global housing_graph, hosts, guests
    
    def fill_edges(self):
        edges = housing_graph.edges()
        random.shuffle(edges)
        for edge in edges: 
            if edge[0] not in [e[0] for e in self.chosen_edges] and edge[1] not in [e[1] for e in self.chosen_edges]:
                self.chosen_edges.append(edge)
        
    def __init__(self):
        self.chosen_edges = []
        self.fill_edges()
    
    def __repr__(self):
        return 'Genome('+str(sorted(self.chosen_edges, key=lambda x: x[0]))+')'
        
    def mutate(self):
        random.shuffle(self.chosen_edges)
        self.chosen_edges = self.chosen_edges[:len(self.chosen_edges)/2]
        self.fill_edges()
    
    def get_clone(self):
        return copy.deepcopy(self)
    
    def get_N_value(self):
        return len(self.chosen_edges)
    
    def get_P_value(self):
        P = 0
        for host in hosts:
            P += len(list_intersection([(host.id_num,preferred_house_guest_id) for preferred_house_guest_id in host.preferred_house_guests], self.chosen_edges))
        for guest in guests:
            host_of_guest_id_num_list = [h for (h,g) in self.chosen_edges if g==guest.id_num]
            assertion(len(host_of_guest_id_num_list)<2, "Guest (id_num: "+str(guest.id_num)+") is assigned to more than one spot.")
            if len(host_of_guest_id_num_list) != 0:
                host_of_guest_id_num = host_of_guest_id_num_list[0]
                host_of_guest = [host for host in hosts if host.id_num==host_of_guest_id_num][0]
                other_host_objects_for_same_host_person = filter(lambda x: same_person(x,host_of_guest), hosts)
                other_host_object_id_nums_for_same_host_person = [host.id_num for host in other_host_objects_for_same_host_person]
                if len(list_intersection(other_host_object_id_nums_for_same_host_person,guest.preferred_house_guests)) > 0:
                    P += 1 # We only add one bc we don't want to double count two host objects that represent the same person
                list_of_co_guests = [g for (h,g) in self.chosen_edges if g != guest.id_num and h in other_host_object_id_nums_for_same_host_person]
                P += len(list_intersection(list_of_co_guests,guest.preferred_house_guests))
        return P

def mate(parent_1, parent_2):
    child = Genome()
    edges_1 = parent_1.chosen_edges
    edges_2 = parent_2.chosen_edges
    random.shuffle(edges_1)
    random.shuffle(edges_2)
    child.chosen_edges=[]
    starting_index_1=0
    starting_index_2=0
    while starting_index_1<len(edges_1)-1 or starting_index_2<len(edges_2)-1:
        for i, edge in enumerate(edges_1[starting_index_1:]):
            if edge[0] not in [e[0] for e in child.chosen_edges] and edge[1] not in [e[1] for e in child.chosen_edges]:
                child.chosen_edges.append(edge)
                break
        starting_index_1+=1+i
        for i, edge in enumerate(edges_2[starting_index_2:]):
            if edge[0] not in [e[0] for e in child.chosen_edges] and edge[1] not in [e[1] for e in child.chosen_edges]:
                child.chosen_edges.append(edge)
                break
        starting_index_2+=1+i
    child.fill_edges()
    return child

def usage(): 
    # Example Usage: python ga.py -population_size 10 -generations 10
    print >> sys.stderr, 'python '+__file__
    print >> sys.stderr, ''
    print >> sys.stderr, 'Options:'
    print >> sys.stderr, '    -population_size: Number of genomes per generation. Default value is '+str(POPULATION_SIZE_DEFAULT_VALUE)+'.'
    print >> sys.stderr, '    -generations: Number of generations. Default value is '+str(GENERATIONS_DEFAULT_VALUE)+'.'
    print >> sys.stderr, '    -tournament_size: Tournament size. Default value is '+str(TOURNAMENT_SIZE_DEFAULT_VALUE)+'.'
    print >> sys.stderr, '    -elite_percent: Percent of the next generation\'s population that will be drawn from elite selection (usage: enter "30" for 30%). Default value is '+str(ELITE_PERCENT_DFAULT_VALUE)+'.'
    print >> sys.stderr, '    -mate_percent: Percent of the next generation\'s population that will be drawn from offspring due to mating (usage: enter "30" for 30%). Default value is '+str(MATE_PERCENT_DEFAULT_VALUE)+'.'
    print >> sys.stderr, '    -mutation_percent: Percent of the next generation\'s population that will be drawn from mutations (usage: enter "30" for 30%). Default value is '+str(MUTATION_PERCENT_DEFAULT_VALUE)+'.'
    print >> sys.stderr, '    -output_dir: Output directory. Default value is '+OUTPUT_DIR_DEFAULT_VALUE+'.'
    
    print >> sys.stderr, ''
    sys.exit(1) 

def main(): 
    start_time = time.time()
    
    if len(sys.argv) < 1: 
        usage() 
    os.system('clear') 
    
    population_size = get_command_line_param_val_default_value(sys.argv, '-population_size', POPULATION_SIZE_DEFAULT_VALUE)
    generations = get_command_line_param_val_default_value(sys.argv, '-generations', GENERATIONS_DEFAULT_VALUE)
    tournament_size = get_command_line_param_val_default_value(sys.argv, '-tournament_size', TOURNAMENT_SIZE_DEFAULT_VALUE)
    elite_percent = get_command_line_param_val_default_value(sys.argv, '-elite_percent', ELITE_PERCENT_DFAULT_VALUE)/100.0
    mate_percent = get_command_line_param_val_default_value(sys.argv, '-mate_percent', MATE_PERCENT_DEFAULT_VALUE)/100.0
    mutation_percent = get_command_line_param_val_default_value(sys.argv, '-mutation_percent', MUTATION_PERCENT_DEFAULT_VALUE)/100.0
    assertion(elite_percent+mate_percent+mutation_percent==1.0,"Sum of elite_percent, mate_percent, and mutation_percent is not equal to 100%.")
    output_dir = get_command_line_param_val_default_value(sys.argv, '-output_dir', OUTPUT_DIR_DEFAULT_VALUE)
    makedirs(output_dir)
    
    print "GA Parameters"
    print "    population_size:", population_size
    print "    generations:", generations
    print "    tournament_size:", tournament_size
    print "    elite_percent: %.2f%%" % (100*elite_percent)
    print "    mate_percent: %.2f%%" % (100*mate_percent)
    print "    mutation_percent: %.2f%%" % (100*mutation_percent)
    print 
    
    global housing_graph, hosts, guests
    
    # Add hosts and guests
    hosts, guests = generate_dummy_hosts_and_guests()
    print "Number of Host Spots:", len(hosts)
    print "Number of Guests:", len(guests)
    print 
    
    # Create Graph
    housing_graph = networkx.Graph()
    
    for host in hosts:
        housing_graph.add_node(host.id_num)
    for guest in guests:
        housing_graph.add_node(guest.id_num)
    
    for host in hosts:
        for guest in guests:
            if are_compatible(host, guest):
                housing_graph.add_edge(host.id_num, guest.id_num) # All of the edges should be ordered in (host,guest) ordering
    
    # Genetic algorithm
    genomes = [Genome() for i in xrange(population_size)]
    maximal_matching = networkx.maximal_matching(housing_graph)
    genomes[-1].chosen_edges=list(maximal_matching)
    genomes[-1].fill_edges()
    
    num_elites = int(round(elite_percent*population_size))
    num_offspring = int(round(mate_percent*population_size))
    num_mutated = int(round(mutation_percent*population_size))
    
    # Save important data
    with open(os.path.join(os.path.abspath(output_dir),'data.py'),'w') as f:
        f.write('hosts='+hosts.__repr__())
        f.write('\n')
        f.write('guests='+guests.__repr__())
    
    max_x = -1
    max_y = -1
    if SAVE_VISUALIZATIONS:
        makedirs(os.path.join(output_dir,'all_generations_point_cloud'))
        makedirs(os.path.join(output_dir,'point_cloud'))
        makedirs(os.path.join(output_dir,'pareto_curves'))
        fig_all_points, subplot_all_points = matplotlib.pyplot.subplots()
        subplot_all_points.set_xlabel('Inverse N Values')
        subplot_all_points.set_ylabel('Inverse P Values')
    for generation in xrange(generations):
        print 
        print "Working on generation", generation
        
        # Save the population
        with open(os.path.join(os.path.abspath(output_dir),'generation_'+str(generation)+'.py'),'w') as f:
            f.write('genomes='+genomes.__repr__())
        
        # Evaluate each population member
        inverse_N_P_scores = sorted([(index, 1.0/(1+genome.get_N_value()), 1.0/(1+genome.get_P_value())) for index,genome in enumerate(genomes)], key=lambda x:x[1]) # sorted from lowest to highest 1/N values
#        print "    Max N: "+str(1/inverse_N_P_scores[-1][1])
#        print "    Max P: "+str(1/max([e[2] for e in inverse_N_P_scores]))
        # Save visualizations
        if SAVE_VISUALIZATIONS:
            if max_x<0 or max_y<0:
                max_x = max([e[1] for e in inverse_N_P_scores])
                max_y = max([e[2] for e in inverse_N_P_scores])
                subplot_all_points.set_xlim(left=0, right=max_x)
                subplot_all_points.set_ylim(bottom=0, top=max_y)
            xy = list(set([e[1:3] for e in inverse_N_P_scores]))
            x = [e[0] for e in xy] # N values
            y = [e[1] for e in xy] # P values
            #Save all points visualization
            subplot_all_points.set_title('Generation '+str(generation))
            subplot_all_points.scatter(x, y, zorder=10, c='c', alpha=0.10)
            fig_all_points.savefig(os.path.join(output_dir,'all_generations_point_cloud/generation_'+str(generation)+'.png'))
            # Save only this generation visualization
            fig, subplot = matplotlib.pyplot.subplots()
            subplot.set_title('Generation '+str(generation))
            subplot.set_xlabel('Inverse N Values')
            subplot.set_ylabel('Inverse P Values')
            subplot.set_xlim(left=0, right=max_x)
            subplot.set_ylim(bottom=0, top=max_y)
            subplot.scatter(x, y, zorder=10, c='r', alpha=1.0)
            fig.savefig(os.path.join(output_dir,'point_cloud/generation_'+str(generation)+'.png'))
        # Get pareto ranking by N and P values
        pareto_ranking = [] 
        if SAVE_VISUALIZATIONS:
            fig_pareto_curves, subplot_pareto_curves = matplotlib.pyplot.subplots()
        for pareto_rank_score in xrange(len(inverse_N_P_scores)): # the number of pareto rank values is upper bounded by the number of points as they all may fall on different pareto curves (imagine if they all lied on the f(x)=x line). 
            indices_to_pop=[]
            prev_inverse_P_score = inf
            for i,(index_of_genome, inverse_N_score, inverse_P_score) in enumerate(sorted(inverse_N_P_scores, key=lambda e:e[1])):
                if inverse_P_score<prev_inverse_P_score:
                    prev_inverse_P_score=inverse_P_score
                    indices_to_pop.append(i)
                    pareto_ranking.append((index_of_genome, pareto_rank_score, inverse_N_score, inverse_P_score))
            if SAVE_VISUALIZATIONS:
                subplot_pareto_curves.set_title('Generation '+str(generation))
                subplot_pareto_curves.set_xlabel('Inverse N Values')
                subplot_pareto_curves.set_ylabel('Inverse P Values')
                subplot_pareto_curves.set_xlim(left=0, right=max_x)
                subplot_pareto_curves.set_ylim(bottom=0, top=max_y)
                xy = sorted(list(set([inverse_N_P_scores[i][1:3] for i in indices_to_pop])), key=lambda e:(e[0],-e[1]))
                x = [e[0] for e in xy] # N values
                y = [e[1] for e in xy] # P values
                color=numpy.random.rand(3,1)
                subplot_pareto_curves.plot(x, y, zorder=10, c=color, alpha=1.0)
                subplot_pareto_curves.scatter(x, y, zorder=10, c=color, alpha=1.0) # points may overlap, and thus some differen colored points may appear on multiple lines, which gives the illusion that the coloring of the points and lines are different.
            for i in indices_to_pop[::-1]:
                inverse_N_P_scores.pop(i)
            if len(inverse_N_P_scores)==0:
                break
        fig_pareto_curves.savefig(os.path.join(output_dir,'pareto_curves/generation_'+str(generation)+'.png'))
        assertion(len(inverse_N_P_scores)==0, "inverse_N_P_scores is not empty after pareto rank determination (all values should've been popped out of it.")
        # Tournament selection for the elites
        elites_scores = []
        tournament_group_start_index=inf
        while len(elites_scores)<num_elites:
            if tournament_group_start_index>len(genomes)-1:
                random.shuffle(pareto_ranking) # tournament groups are selected randomly
                tournament_group_start_index=0
            tournament_group_end_index = min(len(genomes), tournament_group_start_index+tournament_size)
            tournament_group = pareto_ranking[tournament_group_start_index:tournament_group_end_index]
            for genome_pareto_score_set in sorted(tournament_group, key=lambda x:x[1]):
                if genome_pareto_score_set not in elites_scores:
                    elites_scores.append(genome_pareto_score_set)
                    break
            tournament_group_start_index += tournament_size
        elites = [genomes[index_of_genome] for (index_of_genome, pareto_rank_score, inverse_N_score, inverse_P_score) in elites_scores]
        # Random mating 
        offspring=[mate(random.choice(genomes),random.choice(genomes)) for i in xrange(num_offspring)]
        # Random mutation
        mutation=[]
        for genome in random.sample(genomes,num_mutated):
            mutation.append(genome.get_clone())
            mutation[-1].mutate()
        # Create the new generation
        genomes=elites+offspring+mutation
        genomes=genomes[:population_size]
        assertion(len(genomes)==population_size,"len(genomes) is not equal to population_size.")
    
    print 
    print 'Total Run Time: '+str(time.time()-start_time)
    print 

if __name__ == '__main__':
    main()


