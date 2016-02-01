#!/usr/bin/python

'''
Genetic Algorithm for Assigning Housing Spots to Guests for Swing Dancing Events. 

To understand how to use this code, see the usage() function or use "python ga.py -usage" on the commandline. 
'''

import os
import sys
import pdb
import time
from util import *
from ga import GeneticAlgorithm

START_TIME=time.time()

POPULATION_SIZE_DEFAULT_VALUE = 25
NUM_GENERATIONS_DEFAULT_VALUE = 500
NUM_ISLANDS_DEFAULT_VALUE = 1
TOURNAMENT_SIZE_DEFAULT_VALUE = 32
ELITE_PERCENT_DFAULT_VALUE = 80
MATE_PERCENT_DEFAULT_VALUE = 10
MUTATION_PERCENT_DEFAULT_VALUE = 10
OUTPUT_DIR_DEFAULT_VALUE = './output'

def generate_hosts_and_guests(input_xlsx='Housing_Data.xlsx', index_of_sheet_containing_data=0, previously_generated_data='data.py', newly_generated_data='data.py'):
    if os.path.isfile('test_data.py'):
         with open('test_data.py','r') as f:
            host_line, guest_line = f.readlines()
            exec host_line
            exec guest_line
            return hosts, guests
    
    hosts0 = []
    
    workbook = xlrd.open_workbook(input_xlsx)
    sheet = workbook.sheet_by_index(index_of_sheet_containing_data)
    column_names = sheet.row_values(0)
    
    name_index = column_names.index("Name")
    is_host_index = column_names.index("Local Housing")
    num_spots_available_index = column_names.index("How Many People Can You House?")
    late_night_tendencies_index = column_names.index("What is Your Dancing Preference?")
    days_housing_is_available_index = column_names.index("On Which Days Can You Provide Housing?")
    days_housing_is_needed_index = column_names.index("On Which Days Do You Need Housing?")
    has_pets_index = column_names.index("Do You Have Pets?")
    has_allergies_index = column_names.index("Do You Have Pet Allergies?")
    is_smoker_index = column_names.index("Do You Smoke?")
    willing_to_house_with_smokers_index = column_names.index("Acceptable to House with Smokers?")
    willing_to_provide_rides_index = column_names.index("Can You Drive Your Guests to Events?")
    has_ride_index = column_names.index("Do You Need Your Host to Drive You to Events?")
    late_night_tendencies_index = column_names.index("What is Your Dancing Preference?")
    
    for rownum in xrange(1,sheet.nrows):
        line_data = sheet.row_values(rownum)
        if line_data[is_host_index]=="I live in Richmond and would be happy to host fellow Lindy Hoppers because I'm awesome!":
            # This person is a host
            name = line_data[name_index]
            days_housing_is_available = frozenset([e for e in ['Friday', 'Saturday', 'Sunday'] if e in line_data[days_housing_is_available_index]])
            if len(days_housing_is_available)==0:
                continue
            has_cats = 'cats' in line_data[has_pets_index].lower()
            has_dogs = 'dogs' in line_data[has_pets_index].lower()
            willing_to_house_smokers = 'Yes' in line_data[willing_to_house_with_smokers_index]
            willing_to_provide_rides = 'Yes' in line_data[willing_to_provide_rides_index]
            late_night_tendencies = "early sleeper"
            if 'some late night' in line_data[late_night_tendencies_index]:
                late_night_tendencies = "some late night"
            if 'shut down the late night' in line_data[late_night_tendencies_index]:
                late_night_tendencies = "survivors' club"
            num_spots_available = max(0,int(line_data[num_spots_available_index]))
            host_tuple = (Host(
                    name0=name, 
                    email0='NO_EMAIL', 
                    phone_number0='', 
                    days_housing_is_available0=days_housing_is_available,
                    has_cats0=has_cats, 
                    has_dogs0=has_dogs,
                    willing_to_house_smokers0=willing_to_house_smokers, 
                    willing_to_provide_rides0=willing_to_provide_rides, 
                    late_night_tendencies0=late_night_tendencies, 
                    preferred_house_guests0=[], 
                    misc_info0='', 
                    id_num0=generate_unique_identifier()
                ), num_spots_available)
            hosts0.append(host_tuple)
        elif line_data[is_host_index]=="I will be traveling from out-of-town and would appreciate local housing.":
            # This person is a guest
            name = line_data[name_index]
            days_housing_is_needed = frozenset([e for e in ['Friday', 'Saturday', 'Sunday'] if e in line_data[days_housing_is_needed_index]])
            if len(days_housing_is_needed)==0:
                continue
            can_be_around_cats = not 'cats' in line_data[has_allergies_index]
            can_be_around_dogs = not 'dogs' in line_data[has_allergies_index]
            smokes = 'Yes' in line_data[is_smoker_index]
            has_ride = 'No' in line_data[has_ride_index]
            late_night_tendencies = "early sleeper"
            if 'some late night' in line_data[late_night_tendencies_index]:
                late_night_tendencies = "some late night"
            if 'shut down the late night' in line_data[late_night_tendencies_index]:
                late_night_tendencies = "survivors' club"
            misc_info = ''
            guest = Guest(
                        name0=name, 
                        email0='NO_EMAIL', 
                        phone_number0='', 
                        days_housing_is_needed0=days_housing_is_needed,
                        can_be_around_cats0=can_be_around_cats, 
                        can_be_around_dogs0=can_be_around_dogs, 
                        smokes0=smokes, 
                        has_ride0=has_ride, 
                        late_night_tendencies0=late_night_tendencies, 
                        preferred_house_guests0=[], 
                        misc_info0='', 
                        id_num0=generate_unique_identifier()
                    )
            guests.append(guest)
    
    # Generate random preferred house guests
    for host,num_spots_available in random.sample(hosts0, int(len(hosts0)*0.4)): # Let's say 40% of the hosts (people, not spots) prefer guests
        for guest in random.sample(guests, 6): # Let's say the host prefers 6 guests
            host.preferred_house_guests.append(guest.id_num)
    
    for guest in random.sample(guests,int(len(guests)*0.4)): # Let's say 40% of the guests prefer co-guests
        for preferred_guest in random.sample(guests,4): # Let's say the guest prefers 4 co-guests
            guest.preferred_house_guests.append(preferred_guest.id_num)
    
    for guest in random.sample(guests,int(len(guests)*0.4)): # Let's say 40% of the guests prefer hosts
        for preferred_host in random.sample(hosts0,3): # Let's say the guest prefers 3 hosts
            guest.preferred_house_guests.append(preferred_host[0].id_num)
    
    # Clone each host so that there's now one Host object for each spot they have
    for host, num_spots_available in hosts0:
        hosts.append(host)
        for i in xrange(num_spots_available-1):
            clone = host.get_clone()
            clone.id_num = generate_unique_identifier()
            hosts.append(clone)
    
    with open('test_data.py','w') as f:
        f.write('hosts='+hosts.__repr__())
        f.write('\n')
        f.write('guests='+guests.__repr__())
    
    return hosts, guests

#def get_guest_and_host_data(output_dir):
#    
#    # Add hosts and guests
#    hosts, guests = generate_hosts_and_guests()
#    print "Number of Host Spots:", len(hosts)
#    print "Number of Guests:", len(guests)
#    print 
#    
#    # Save host and guest data
#    with open(join_paths([os.path.abspath(output_dir),'data.py']),'w') as f:
#        f.write('hosts='+hosts.__repr__())
#        f.write('\n')
#        f.write('guests='+guests.__repr__())
#    
#    # Create Graph
#    housing_graph = networkx.DiGraph()
#    
#    for host in hosts:
#        housing_graph.add_node(host.id_num)
#    for guest in guests:
#        housing_graph.add_node(guest.id_num)
#    
#    for host in hosts:
#        for guest in guests:
#            if are_compatible(host, guest):
#                housing_graph.add_edge(host.id_num, guest.id_num) # All of the edges should be ordered in (host,guest) ordering

def usage(): 
    # Example Usage: python ga.py -population_size 100 -num_generations 100 -output_dir ./output
    print >> sys.stderr, 'python '+__file__+' <options>'
    print >> sys.stderr, ''
    print >> sys.stderr, 'Options:'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -population_size <int>'
    print >> sys.stderr, '        Number of genomes per generation. Default value is '+str(POPULATION_SIZE_DEFAULT_VALUE)+'.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -num_generations <int>'
    print >> sys.stderr, '        Number of generations. Default value is '+str(NUM_GENERATIONS_DEFAULT_VALUE)+'.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -num_islands <int>'
    print >> sys.stderr, '        Number of islands. Default value is '+str(NUM_ISLANDS_DEFAULT_VALUE)+'.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -tournament_size <int>'
    print >> sys.stderr, '        Tournament size. Default value is '+str(TOURNAMENT_SIZE_DEFAULT_VALUE)+'.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -elite_percent <float>'
    print >> sys.stderr, '        Percent of the next generation\'s population to be drawn from elite selection (usage: enter "30.0" for 30%). Default value is '+str(ELITE_PERCENT_DFAULT_VALUE)+'.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -mate_percent <float>'
    print >> sys.stderr, '        Percent of the next generation\'s population to be drawn from offspring due to mating (usage: enter "30.0" for 30%). Default value is '+str(MATE_PERCENT_DEFAULT_VALUE)+'.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -mutation_percent <float>'
    print >> sys.stderr, '        Percent of the next generation\'s population to be drawn from mutations (usage: enter "30.0" for 30%). Default value is '+str(MUTATION_PERCENT_DEFAULT_VALUE)+'.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -output_dir <string>'
    print >> sys.stderr, '        Output directory. Default value is '+OUTPUT_DIR_DEFAULT_VALUE+'.'
    print >> sys.stderr, ''
    sys.exit(1) 

def main():
    print '\n'*100 # Clear
    
    if len(sys.argv) < 1 or '-usage' in sys.argv: 
        usage()
    
    population_size = int(get_command_line_param_val_default_value(sys.argv, '-population_size', POPULATION_SIZE_DEFAULT_VALUE))
    num_generations = int(get_command_line_param_val_default_value(sys.argv, '-num_generations', NUM_GENERATIONS_DEFAULT_VALUE))
    num_islands = int(get_command_line_param_val_default_value(sys.argv, '-num_islands', NUM_ISLANDS_DEFAULT_VALUE))
    tournament_size = int(get_command_line_param_val_default_value(sys.argv, '-tournament_size', TOURNAMENT_SIZE_DEFAULT_VALUE))
    elite_percent = float(get_command_line_param_val_default_value(sys.argv, '-elite_percent', ELITE_PERCENT_DFAULT_VALUE))/100.0
    mate_percent = float(get_command_line_param_val_default_value(sys.argv, '-mate_percent', MATE_PERCENT_DEFAULT_VALUE))/100.0
    mutation_percent = float(get_command_line_param_val_default_value(sys.argv, '-mutation_percent', MUTATION_PERCENT_DEFAULT_VALUE))/100.0
    assertion(elite_percent+mate_percent+mutation_percent==1.0,"Sum of elite_percent, mate_percent, and mutation_percent is not equal to 100%.")
    output_dir = os.path.abspath(get_command_line_param_val_default_value(sys.argv, '-output_dir', OUTPUT_DIR_DEFAULT_VALUE))
    makedirs(output_dir)
    
    print "GA Parameters"
    print "    population_size:", population_size
    print "    num_generations:", num_generations
    print "    num_islands:", num_islands
    print "    tournament_size:", tournament_size
    print "    elite_percent: %.2f%%" % (100*elite_percent)
    print "    mate_percent: %.2f%%" % (100*mate_percent)
    print "    mutation_percent: %.2f%%" % (100*mutation_percent)
    print "    output_dir:", output_dir
    print 
    
    ga = GeneticAlgorithm(population_size, tournament_size, elite_percent, mate_percent, mutation_percent)
    
    print 
    print 'Total Run Time: '+str(time.time()-START_TIME)
    print 

if __name__ == '__main__':
    main()

