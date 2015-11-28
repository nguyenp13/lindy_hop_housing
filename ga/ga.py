#!/usr/bin/python

'''
TODO:
    Very Important
        get Genome class running
        Add parsing of real data to add real hosts and guests instead of using the dummy func
    
    Less Important
        add __repr__ method for Host, Guest, and Genome
'''

import os
import sys
import pdb
import networkx
import time
import random
from util import *

class Host(object):
    def __init__(self, name0='NO_NAME', email0='NO_EMAIL', phone_number0='', days_housing_is_available0=frozenset(), number_of_spots0=0, has_cats0=False, has_dogs0=False, willing_to_house_smokers0=True, willing_to_provide_rides0=False, late_night_tendencies0="survivors' club", misc_info0='', id_num0=-1):
        self.name=name0
        self.email=email0
        self.phone_number=phone_number0 # is a string
        self.days_housing_is_available=days_housing_is_available0 # is a frozenset
        self.number_of_spots=number_of_spots0
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
    Number of Available Spots: '''+str(self.number_of_spots)+'''
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

class Genome(object):
    def __init__(self, graph0):
        self.graph=graph0
    
    def __str__(self):
        ans = 'String method for genome not yet defined.'
        return ans.strip('\n')
    
    def mutate(self):
        assertion(False, "Mutate method not yet defined.")

def generate_fixed_dummy_hosts_and_guests():
    hosts=[]
    guests=[]
    
#    hosts.append(
#        Host(
#                name0='Dummy Host '+str(1), 
#                email0='dummy_host_email'+str(1)+'@dummy.domain.com', 
#                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
#                days_housing_is_available0=frozenset(['Friday','Saturday','Sunday']), 
#                number_of_spots0=1,
#                has_cats0=False, 
#                has_dogs0=False, 
#                willing_to_house_smokers0=True, 
#                willing_to_provide_rides0=True, 
#                late_night_tendencies0="survivors' club", 
#                misc_info0='Dummy Misc. Info. for Dummy Host '+str(1),
#                id_num0=generate_unique_identifier()
#            )
#        )
#    
#    hosts.append(
#        Host(
#                name0='Dummy Host '+str(2), 
#                email0='dummy_host_email'+str(2)+'@dummy.domain.com', 
#                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
#                days_housing_is_available0=frozenset(['Friday','Saturday','Sunday']), 
#                number_of_spots0=1,
#                has_cats0=False, 
#                has_dogs0=False, 
#                willing_to_house_smokers0=True, 
#                willing_to_provide_rides0=True, 
#                late_night_tendencies0="survivors' club", 
#                misc_info0='Dummy Misc. Info. for Dummy Host '+str(2),
#                id_num0=generate_unique_identifier()
#            )
#        )
#    
#    guests.append(
#        Guest(
#                name0='Dummy Guest '+str(3), 
#                email0='dummy_guest_email'+str(3)+'@dummy.domain.com', 
#                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
#                days_housing_is_needed0=frozenset(['Friday','Saturday','Sunday']), 
#                can_be_around_cats0=True, 
#                can_be_around_dogs0=True, 
#                smokes0=False, 
#                has_ride0=True, 
#                late_night_tendencies0="survivors' club", 
#                misc_info0='Dummy Mist. Info. for Dummy Host '+str(3),
#                id_num0=generate_unique_identifier()
#            )
#        )
#    
#    guests.append(
#        Guest(
#                name0='Dummy Guest '+str(4), 
#                email0='dummy_guest_email'+str(4)+'@dummy.domain.com', 
#                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
#                days_housing_is_needed0=frozenset(['Friday','Saturday','Sunday']), 
#                can_be_around_cats0=True, 
#                can_be_around_dogs0=True, 
#                smokes0=False, 
#                has_ride0=True, 
#                late_night_tendencies0="survivors' club", 
#                misc_info0='Dummy Mist. Info. for Dummy Host '+str(4),
#                id_num0=generate_unique_identifier()
#            )
#        )
    
    hosts.append(
        Host(
                name0='Dummy Host '+str(5), 
                email0='dummy_host_email'+str(5)+'@dummy.domain.com', 
                phone_number0=reduce(lambda x,y:x+y,[str(random.randint(0,9)) for ii in xrange(10)]), 
                days_housing_is_available0=frozenset(['Friday','Saturday','Sunday']), 
                number_of_spots0=1,
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
                misc_info0='Dummy Mist. Info. for Dummy Host '+str(7),
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
                number_of_spots0=1,
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
    hosts, guests = generate_fixed_dummy_hosts_and_guests()
    
    # Create Graph
    G = networkx.Graph()
    
    for host in hosts:
        G.add_node(host.id_num)
    for guest in guests:
        G.add_node(guest.id_num)
    
    for host in hosts:
        for guest in guests:
            if are_compatible(host, guest):
                G.add_edge(host.id_num, guest.id_num)
    
    print G.nodes()
    print G.edges()
    
    genomes = [Genome(G) for i in xrange(population_size)]
    
    print 'Total Run Time: '+str(time.time()-start_time)
    print 

if __name__ == '__main__':
    main()
