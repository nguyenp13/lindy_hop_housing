#!/usr/bin/python

'''
TODO:
    Very Important
        Add parsing of real data to add real hosts and guests instead of using the dummy func
            parse the real data so that we have a list of edges (host,guest) of people hat prefer each other so that we can easily see which guests and hosts prefer each other. this willmake determing p values easier. determining guests who prefer guests will still take a while
            get the P value determination method added to the genome class
        Implement finding P values for guests that prefer each other
        Save the __repr__() values of the genomes for each generation in text files
        create a pareto curve image for each generation that includes points for each previously generated genome
    
    Less Important
        Get late night tendencies to be taken into account for the P value determination
        add preferred_house_guests to the __str__() method of Guest and Host
            make it look up in the hosts and guests global list variables for the names of the actual preferred house guests 
'''

import os
import sys
import pdb
import networkx
import time
import random
import copy
from util import *

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

def generate_fixed_dummy_hosts_and_guests():
    hosts=[
        Host(name0='Host 1', id_num0=1),
        Host(name0='Host 2', preferred_house_guests0=[4,5], id_num0=2),
        Host(name0='Host 3', id_num0=3),
    ]
    guests=[
        Guest(name0='Guest 4', preferred_house_guests0=[2,5], id_num0=4),
        Guest(name0='Guest 5', preferred_house_guests0=[2,4], id_num0=5),
        Guest(name0='Guest 6', id_num0=6),
    ]
    return hosts, guests

class Genome(object):
    
    global housing_graph, hosts, guests
    
    def fill_edges(self):
        edges = housing_graph.edges()
        random.shuffle(edges)
        for edge in edges: 
            if edge[0] not in [e[0] for e in self.chosen_edges] and edge[1] not in [e[1] for e in self.chosen_edges]:
                self.chosen_edges.append(edge)
        
    def __init__(self, initial_edges=[]):
        self.chosen_edges = initial_edges
        self.fill_edges()
    
    def __repr__(self):
        return 'Genome('+str(sorted(self.chosen_edges, key=lambda x: x[0]))+')'
        
    def mutate(self):
        random.shuffle(self.chosen_edges)
        self.chosen_edges = self.chosen_edges[:len(self.chosen_edges)/2]
        self.fill_edges()
    
    def get_num_housed_guests(self):
        return len(self.chosen_edges)
    
    def get_P_value(self):
        P = 0
        for host in hosts:
            P += len(list_intersection([(host.id_num,preferred_house_guest_id) for preferred_house_guest_id in host.preferred_house_guests],chosen_edges))
        # Can't implement finding P values of guests that prefer each other bc each Host object actually prepresents a spot in a host's house, not necessarily just one host. 
        
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
    print >> sys.stderr, '    -population_size: Number of genomes per generation.'
    print >> sys.stderr, '    -generations: Number of generations.'
    print >> sys.stderr, ''
    sys.exit(1) 

def main(): 
    start_time = time.time()
    
    if len(sys.argv) < 1: 
        usage() 
    os.system('clear') 
    
    population_size = get_command_line_param_val_default_value(sys.argv, '-population_size', 10)
    generations = get_command_line_param_val_default_value(sys.argv, '-generations', 10)
    global housing_graph, hosts, guests
    
    # Add hosts and guests
    hosts, guests = generate_fixed_dummy_hosts_and_guests()
    
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
    
    maximal_matching = networkx.maximal_matching(housing_graph)
    print "Nodes:", housing_graph.nodes()
    print "Edges:", housing_graph.edges()
    print "Maximal Matching:", maximal_matching
    print 
    
    genomes = [Genome() for i in xrange(population_size)]
    for i,g in enumerate(genomes):
        print i, g
    print '\n'
    for g in genomes:
        g.mutate()
    for i,g in enumerate(genomes):
        print i, g
    print '\n'
    
    child = mate(genomes[0],genomes[1])
    print 'Parent 1:', genomes[0]
    print 'Parent 2:', genomes[1]
    print 'Child:', child
    
    print guests[0].__str__()
    print guests[0].__repr__()
    
    print hosts[0].__str__()
    print hosts[0].__repr__()
    
    print 
    print hosts.__repr__()
    
    print 
    print 'Total Run Time: '+str(time.time()-start_time)
    print 

if __name__ == '__main__':
    main()


