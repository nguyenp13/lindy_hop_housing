#!/usr/bin/python

'''

Genetic Algorithm for Assigning Housing Spots to Guests for Swing Dancing Events. 

To understand how to use this code, see the usage() function or use "python ga.py -usage" on the commandline. 

TODO: 
    GeneticAlgorithm() code
        create genomes class
        create method for GeneticAlgorithm() to run one generation
    Finish coding get_misc_info()
'''

import os
import sys
import pdb
import time
import GeneticAlgorithm
from util import *

START_TIME=time.time()

DEBUG = False
EVENT_WE_ARE_HOUSING_FOR='RLX' # Value should be "The Process" or "RLX"

INPUT_XLSX_FILE_NAME_DEFAULT_VALUE = "raw_housing_data.xlsx"
POPULATION_SIZE_DEFAULT_VALUE = 25
NUM_GENERATIONS_DEFAULT_VALUE = 500
NUM_ISLANDS_DEFAULT_VALUE = 1
TOURNAMENT_SIZE_DEFAULT_VALUE = 32
ELITE_PERCENT_DFAULT_VALUE = 80
MATE_PERCENT_DEFAULT_VALUE = 10
MUTATION_PERCENT_DEFAULT_VALUE = 10
OUTPUT_DIR_DEFAULT_VALUE = './output'

def get_hosts_and_guests(input_xlsx='housing_data.xlsx', index_of_sheet_containing_data=0):
    previously_generated_data_file_name = remove_file_extension(input_xlsx+'_parsed.py')
    if os.path.isfile(previously_generated_data_file_name):
         with open(previously_generated_data_file_name,'r') as f:
            line=f.readlines()[0]
            if 'dict_of_hosts, dict_of_guests, dict_of_host_spots=(' in line:
                d = {}
                exec line in globals(), d
                return d['dict_of_hosts'], d['dict_of_guests'], d['dict_of_host_spots']
    
    workbook = xlrd.open_workbook(input_xlsx)
    sheet = workbook.sheet_by_index(index_of_sheet_containing_data)
    column_names = sheet.row_values(0)
    
    time_registered_index = column_names.index("Time")
    first_name_index = column_names.index("Name (First)")
    last_name_index = column_names.index("Name (Last)")
    email_index = column_names.index("Email")
    is_host_index = column_names.index("Local Housing")
    events_registered_index = column_names.index("For Which Event(s) Would You Like to Register?")
    events_doing_housing_index = column_names.index("For Which Event(s) Can You Provide Housing?")
    events_needing_housing_index = column_names.index("For Which Event(s) Would You Like Local Housing?")
    rlx_additional_comments_index = column_names.index("RLX - Additional Comments (Optional)")
    late_night_tendencies_index = column_names.index("What is Your Dancing Preference?")
    gender_index = column_names.index("Gender")
    hosts_prefer_which_gender_index = column_names.index("Which Gender Would You Prefer to House?")
    guests_prefer_which_gender_index = column_names.index("With Which Gender Would You Prefer to House?")
    days_housing_is_available_index = column_names.index("On Which Days Can You Provide Housing?")
    days_housing_is_needed_index = column_names.index("On Which Days Do You Need Housing?")
    num_spots_available_index = column_names.index("How Many People Can You House?")
    is_smoker_index = column_names.index("Do You Smoke?")
    willing_to_house_smokers_index = column_names.index("Acceptable to House with Smokers?")
    has_allergies_index = column_names.index("Do You Have Pet Allergies?")
    has_pets_index = column_names.index("Do You Have Pets?")
    has_ride_index = column_names.index("Do You Need Your Host to Drive You to Events?")
    willing_to_provide_rides_index = column_names.index("Can You Drive Your Guests to Events?")
    phone_number_index = column_names.index("Phone (Optional)")
    hometown_index = column_names.index("Hometown (Optional)")
    additional_comments_index = column_names.index("Additional Comments About Housing (Optional)")
    preferred_housing_buddies_index = column_names.index("Preferred Housing Buddies")
    
    dict_of_hosts=dict()
    dict_of_guests=dict()
    dict_of_host_spots=dict()
    dict_hosts_to_host_spots=dict()
    
    for rownum in xrange(1,sheet.nrows):
        line_data = sheet.row_values(rownum)
        if line_data[is_host_index]=="I live in Richmond and would be happy to host fellow Lindy Hoppers because I'm awesome!":
            # This person is a host
            time_registered = line_data[time_registered_index]
            first_name = line_data[first_name_index].strip()
            last_name = line_data[last_name_index].strip()
            email = line_data[email_index]
            events_registered = [] # Currently, our data has no one who is registed for the Process, but not RLX
            if "Both RLX and The Process (save $10!)" in line_data[events_registered_index]:
                events_registered += ["The Process", "RLX"]
            if "RLX 2016" in line_data[events_registered_index]:
                events_registered += ["RLX"]
            events_doing_housing = [] # Currently, our data has no one who is housing people for the Process, but not RLX
            if "Both RLX and The Process!" in line_data[events_doing_housing_index]:
                events_doing_housing += ["The Process", "RLX"]
            if "RLX 2016" in line_data[events_doing_housing_index]:
                events_doing_housing += ["RLX"]
            rlx_additional_comments = line_data[rlx_additional_comments_index]
            late_night_tendencies = "early sleeper"
            if 'some late night' in line_data[late_night_tendencies_index]:
                late_night_tendencies = "some late night"
            if 'shut down the late night' in line_data[late_night_tendencies_index]:
                late_night_tendencies = "survivors' club"
            gender = line_data[gender_index]
            hosts_prefer_which_gender = line_data[hosts_prefer_which_gender_index]
            days_housing_is_available = frozenset([e for e in ['Friday', 'Saturday', 'Sunday'] if e in line_data[days_housing_is_available_index]])
            if len(days_housing_is_available)==0:
                continue
            num_spots_available = min(10, max(0,int(line_data[num_spots_available_index])))
            willing_to_house_smokers = 'Yes' in line_data[willing_to_house_smokers_index]
            has_cats = 'cats' in line_data[has_pets_index].lower()
            has_dogs = 'dogs' in line_data[has_pets_index].lower()
            willing_to_provide_rides = 'Yes' in line_data[willing_to_provide_rides_index]
            phone_number = line_data[phone_number_index]
            hometown = line_data[hometown_index]
            additional_comments = line_data[additional_comments_index]
            preferred_housing_buddies = frozenset(map(lambda x: x.strip(), line_data[preferred_housing_buddies_index].split(',')))
            
            current_host_id_num=rownum+1 # the +1 is to make sure the id_num matches the row number in the excel sheet
            dict_of_hosts[current_host_id_num] = \
                {
                    "time_registered": time_registered, 
                    "first_name": first_name, 
                    "last_name": last_name, 
                    "email": email, 
                    "events_registered": events_registered, 
                    "events_doing_housing": events_doing_housing, 
                    "rlx_additional_comments": rlx_additional_comments, 
                    "late_night_tendencies": late_night_tendencies, 
                    "gender": gender, 
                    "hosts_prefer_which_gender": hosts_prefer_which_gender, 
                    "days_housing_is_available": days_housing_is_available, 
                    "num_spots_available": num_spots_available, 
                    "willing_to_house_smokers": willing_to_house_smokers, 
                    "has_cats": has_cats, 
                    "has_dogs": has_dogs, 
                    "willing_to_provide_rides": willing_to_provide_rides, 
                    "phone_number": phone_number, 
                    "hometown": hometown, 
                    "additional_comments": additional_comments, 
                    "preferred_housing_buddies": preferred_housing_buddies, 
                }
            
            if DEBUG: # Debug Prints
                dict_pretty_print(dict_of_hosts[current_host_id_num])
            
            dict_hosts_to_host_spots[current_host_id_num] = []
            for _ in xrange(num_spots_available):
                host_spot_id_num=generate_unique_identifier()
                dict_of_host_spots[host_spot_id_num] = current_host_id_num
                dict_hosts_to_host_spots[current_host_id_num].append(host_spot_id_num)
        elif line_data[is_host_index]=="I will be traveling from out-of-town and would appreciate local housing.":
            # This person is a guest
            time_registered = line_data[time_registered_index]
            first_name = line_data[first_name_index].strip()
            last_name = line_data[last_name_index].strip()
            email = line_data[email_index]
            events_registered = [] # Currently, our data has no one who is registed for the Process, but not RLX
            if "Both RLX and The Process (save $10!)" in line_data[events_registered_index]:
                events_registered += ["The Process", "RLX"]
            if "RLX 2016" in line_data[events_registered_index]:
                events_registered += ["RLX"]
            events_needing_housing = [] # Currently, our data has no one who is housing people for the Process, but not RLX
            if "Both RLX and The Process!" in line_data[events_needing_housing_index]:
                events_needing_housing += ["The Process", "RLX"]
            if "RLX 2016" in line_data[events_needing_housing_index]:
                events_needing_housing += ["RLX"]
            rlx_additional_comments = line_data[rlx_additional_comments_index]
            late_night_tendencies = "early sleeper"
            if 'some late night' in line_data[late_night_tendencies_index]:
                late_night_tendencies = "some late night"
            if 'shut down the late night' in line_data[late_night_tendencies_index]:
                late_night_tendencies = "survivors' club"
            gender = line_data[gender_index]
            guests_prefer_which_gender = line_data[guests_prefer_which_gender_index]
            days_housing_is_needed = frozenset([e for e in ['Friday', 'Saturday', 'Sunday'] if e in line_data[days_housing_is_needed_index]])
            if len(days_housing_is_needed)==0:
                continue
            smokes = 'Yes' in line_data[is_smoker_index]
            can_be_around_cats = not 'cats' in line_data[has_allergies_index]
            can_be_around_dogs = not 'dogs' in line_data[has_allergies_index]
            has_ride = 'No' in line_data[has_ride_index]
            phone_number = line_data[phone_number_index]
            hometown = line_data[hometown_index]
            additional_comments = line_data[additional_comments_index]
            preferred_housing_buddies = frozenset(map(lambda x: x.strip(), line_data[preferred_housing_buddies_index].split(',')))
            
            current_guest_id_num=rownum+1 # the +1 is to make sure the id_num matches the row number in the excel sheet
            dict_of_guests[current_guest_id_num] = \
                {
                    "first_name": first_name, 
                    "last_name": last_name, 
                    "email": email, 
                    "events_registered": events_registered, 
                    "events_needing_housing": events_needing_housing, 
                    "rlx_additional_comments": rlx_additional_comments, 
                    "late_night_tendencies": late_night_tendencies, 
                    "gender": gender, 
                    "guests_prefer_which_gender": guests_prefer_which_gender, 
                    "days_housing_is_needed": days_housing_is_needed, 
                    "smokes": smokes, 
                    "can_be_around_cats": can_be_around_cats, 
                    "can_be_around_dogs": can_be_around_dogs, 
                    "has_ride": has_ride, 
                    "phone_number": phone_number, 
                    "hometown": hometown, 
                    "additional_comments": additional_comments, 
                    "preferred_housing_buddies": preferred_housing_buddies, 
                }
                
            if DEBUG: # Debug Prints
                dict_pretty_print(dict_of_guests[current_guest_id_num])
            
    return dict_of_hosts, dict_of_guests, dict_of_host_spots, dict_hosts_to_host_spots 

def usage(): 
    # Example Usage: python ga.py -population_size 100 -num_generations 100 -output_dir ./output
    print >> sys.stderr, 'Usage: python '+__file__+' <options>'
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
    
    input_xlsx_file_name = get_command_line_param_val_default_value(sys.argv, '-mutation_percent', INPUT_XLSX_FILE_NAME_DEFAULT_VALUE)
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
    print "    input_xlsx_file_name:", input_xlsx_file_name
    print "    population_size:", population_size
    print "    num_generations:", num_generations
    print "    num_islands:", num_islands
    print "    tournament_size:", tournament_size
    print "    elite_percent: %.2f%%" % (100*elite_percent)
    print "    mate_percent: %.2f%%" % (100*mate_percent)
    print "    mutation_percent: %.2f%%" % (100*mutation_percent)
    print "    output_dir:", output_dir
    print 
    
    dict_of_hosts, dict_of_guests, dict_of_host_spots, dict_hosts_to_host_spots  = get_hosts_and_guests(input_xlsx_file_name)
    
    print "Housing data has been parsed."
    print "    Number of Hosts: "+str(len(dict_of_hosts))
    print "    Number of Spots for Guests: "+str(len(dict_of_host_spots))
    print "    Number of Guests: "+str(len(dict_of_guests))
    
    ga = GeneticAlgorithm.GeneticAlgorithm(dict_of_hosts, dict_of_guests, dict_of_host_spots, dict_hosts_to_host_spots, population_size, tournament_size, elite_percent, mate_percent, mutation_percent)
    
    print 
    print 'Total Run Time: '+str(time.time()-START_TIME)
    print 

if __name__ == '__main__':
    main()

