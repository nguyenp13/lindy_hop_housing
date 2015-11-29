#!/usr/bin/python

'''
TODO:
    Very Important
        get Genome class running
            get mate() func working
        Add parsing of real data to add real hosts and guests instead of using the dummy func
            implement feature to have lists of preferred guests and hosts via a list of id_num values
            then get the P value determination method added to the genome class
    
    Less Important
        add __repr__ method for Host, Guest, and Genome
        add __str__ for Genome
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

class Host(object):
    def __init__(self, name0='NO_NAME', email0='NO_EMAIL', phone_number0='', days_housing_is_available0=frozenset(), has_cats0=False, has_dogs0=False, willing_to_house_smokers0=True, willing_to_provide_rides0=False, late_night_tendencies0="survivors' club", misc_info0='', id_num0=-1):
        self.name=name0
        self.email=email0
        self.phone_number=phone_number0 # is a string
        self.days_housing_is_available=days_housing_is_available0 # is a frozenset
        self.has_cats=has_cats0
        self.has_dogs=has_dogs0
        self.willing_to_house_smokers=willing_to_house_smokers0
        self.willing_to_provide_rides=willing_to_provide_rides0
        self.late_night_tendencies=late_night_tendencies0 # is a string
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
    Days Housing Is Available: '''+(('Friday,' if 'Friday' in self.days_housing_is_available else '')+('Saturday,' if 'Saturday' in self.days_housing_is_available else '')+('Sunday,' if 'Sunday' in self.days_housing_is_available else ''))[:-1]+'''
    Has Cats: '''+('Yes' if self.has_cats else 'No')+'''
    Has Dogs: '''+('Yes' if self.has_dogs else 'No')+'''
    Willing to House Smokers: '''+('Yes' if self.willing_to_house_smokers else 'No')+''' 
    Willing to Provide Rides: '''+('Yes' if self.willing_to_provide_rides else 'No')+'''
    Late Night Tendencies: '''+self.late_night_tendencies+'''
    Misc. Info.: '''+self.misc_info+'''
'''
        return ans

class Guest(object):
    def __init__(self, name0='NO_NAME', email0='NO_EMAIL', phone_number0='', days_housing_is_needed0=frozenset(), can_be_around_cats0=False, can_be_around_dogs0=False, smokes0=True, has_ride0=False, late_night_tendencies0="survivors' club", misc_info0='', id_num0=-1):
        self.name=name0
        self.email=email0
        self.phone_number=phone_number0 # is a string
        self.days_housing_is_needed=days_housing_is_needed0 # is a frozenset
        self.can_be_around_cats=can_be_around_cats0
        self.can_be_around_dogs=can_be_around_dogs0
        self.smokes=smokes0
        self.has_ride=has_ride0
        self.late_night_tendencies=late_night_tendencies0 # is a string
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
    hosts=[]
    guests=[]
    
    hosts.append(
        Host(
                name0='Dummy Host '+str(1), 
                email0='dummy_host_email'+str(1)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_available0=frozenset(['Friday','Saturday','Sunday']), 
                has_cats0=False, 
                has_dogs0=False, 
                willing_to_house_smokers0=True, 
                willing_to_provide_rides0=True, 
                late_night_tendencies0="survivors' club", 
                misc_info0='Dummy Misc. Info. for Dummy Host '+str(1),
                id_num0=generate_unique_identifier()
            )
        )
    
    hosts.append(
        Host(
                name0='Dummy Host '+str(2), 
                email0='dummy_host_email'+str(2)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_available0=frozenset(['Friday','Saturday','Sunday']), 
                has_cats0=False, 
                has_dogs0=False, 
                willing_to_house_smokers0=True, 
                willing_to_provide_rides0=True, 
                late_night_tendencies0="survivors' club", 
                misc_info0='Dummy Misc. Info. for Dummy Host '+str(2),
                id_num0=generate_unique_identifier()
            )
        )
    
    guests.append(
        Guest(
                name0='Dummy Guest '+str(3), 
                email0='dummy_guest_email'+str(3)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_needed0=frozenset(['Friday','Saturday','Sunday']), 
                can_be_around_cats0=True, 
                can_be_around_dogs0=True, 
                smokes0=False, 
                has_ride0=True, 
                late_night_tendencies0="survivors' club", 
                misc_info0='Dummy Mist. Info. for Dummy Host '+str(3),
                id_num0=generate_unique_identifier()
            )
        )
    
    guests.append(
        Guest(
                name0='Dummy Guest '+str(4), 
                email0='dummy_guest_email'+str(4)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_needed0=frozenset(['Friday','Saturday','Sunday']), 
                can_be_around_cats0=True, 
                can_be_around_dogs0=True, 
                smokes0=False, 
                has_ride0=True, 
                late_night_tendencies0="survivors' club", 
                misc_info0='Dummy Mist. Info. for Dummy Host '+str(4),
                id_num0=generate_unique_identifier()
            )
        )
    
    hosts.append(
        Host(
                name0='Dummy Host '+str(5), 
                email0='dummy_host_email'+str(5)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_available0=frozenset(['Friday','Saturday','Sunday']), 
                has_cats0=False, 
                has_dogs0=False, 
                willing_to_house_smokers0=True, 
                willing_to_provide_rides0=True, 
                late_night_tendencies0="survivors' club", 
                misc_info0='Dummy Misc. Info. for Dummy Host '+str(5),
                id_num0=generate_unique_identifier()
            )
        )
    
    guests.append(
        Guest(
                name0='Dummy Guest '+str(6), 
                email0='dummy_guest_email'+str(6)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_needed0=frozenset(['Friday','Saturday','Sunday']), 
                can_be_around_cats0=True, 
                can_be_around_dogs0=True, 
                smokes0=False, 
                has_ride0=True, 
                late_night_tendencies0="survivors' club", 
                misc_info0='Dummy Mist. Info. for Dummy Host '+str(6),
                id_num0=generate_unique_identifier()
            )
        )
    
    return hosts, guests

def generate_random_dummy_hosts_and_guests(num_hosts=10, num_guests=10):
    hosts = [Host(
                name0='Dummy Host '+str(i), 
                email0='dummy_host_email'+str(i)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_available0=frozenset(['Friday','Saturday','Sunday']), 
                has_cats0=False, 
                has_dogs0=False, 
                willing_to_house_smokers0=True, 
                willing_to_provide_rides0=True, 
                late_night_tendencies0="survivors' club", 
                misc_info0='Dummy Misc. Info. for Dummy Host '+str(i),
                id_num0=generate_unique_identifier()
                )
            for i in xrange(num_hosts)]
    guests = [Guest(
                name0='Dummy Guest '+str(i), 
                email0='dummy_guest_email'+str(i)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_needed0=frozenset(['Friday','Saturday','Sunday']), 
                can_be_around_cats0=True, 
                can_be_around_dogs0=True, 
                smokes0=False, 
                has_ride0=True, 
                late_night_tendencies0="survivors' club", 
                misc_info0='Dummy Mist. Info. for Dummy Host '+str(i),
                id_num0=generate_unique_identifier()
                )
            for i in xrange(num_guests)]
    return hosts, guests

class Genome(object):
    
    global housing_graph
    
    def fill_edges(self):
        edges = housing_graph.edges()
        random.shuffle(edges)
        for edge in edges: 
            if edge[0] not in [e[0] for e in self.chosen_edges] and edge[1] not in [e[1] for e in self.chosen_edges]:
                self.chosen_edges.append(edge)
        
    def __init__(self):
        self.chosen_edges = []
        self.fill_edges()
    
    def __str__(self):
        ans = 'String method for genome not yet defined.'
        return ans
    
    def mutate(self):
        random.shuffle(self.chosen_edges)
        self.chosen_edges = self.chosen_edges[:len(self.chosen_edges)/2]
        self.fill_edges()
    
    def get_num_housed_guests(self):
        return len(self.chosen_edges)

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
    
    # Add hosts and guests
#    hosts, guests = generate_random_dummy_hosts_and_guests()
#    hosts, guests = generate_fixed_dummy_hosts_and_guests()
    hosts, guests = generate_random_dummy_hosts_and_guests(3,3)
    
    # Create Graph
    global housing_graph
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
        print i, sorted(g.chosen_edges, key=lambda x: x[0])
    print '\n'
    for g in genomes:
        g.mutate()
    for i,g in enumerate(genomes):
        print i, sorted(g.chosen_edges, key=lambda x: x[0])
    print '\n'
    
    child = mate(genomes[0],genomes[1])
    print 'Parent 1:', sorted(genomes[0].chosen_edges, key=lambda x: x[0])
    print 'Parent 2:', sorted(genomes[1].chosen_edges, key=lambda x: x[0])
    print 'Child:', sorted(child.chosen_edges, key=lambda x: x[0])
    
    print 
    print 'Total Run Time: '+str(time.time()-start_time)
    print 

if __name__ == '__main__':
    main()
