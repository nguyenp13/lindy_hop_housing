#!/usr/bin/python

'''
TODO:
    Very Important
        Add gender to teh host and guest classes
        add a person_id for each host to make telling if the hosts are teh same faster as well as making it easier to determine who else is staying with the host
        update the tips and hacks to explain the P and N concepts
        change it so that the hosts and guests are no longer lists but dictionaries where the key is the person's id_num
        
        Change the code so that it takes place in several stages
            step 1: preprocessing the data
                we will always need to go through the initial data anyway to read Misc. Comments. 
                our code will go through and tell if there are any problems with any entries, the user will have to fix them. 
                    problems can be bad data types, mispelled preferred co-guest names, etc. 
                during this initial phase, it should be noted that the user must add in manually if any two people can't stay together for specific reasons
            step 2: we run our GA
            Step 3: we print out our results for each solution we have
                we will state what things we could not obey when determing P, e.g. preferred guests they couldn't stay with, different late night tendencies, etc. It should be easily read by our user
        
        we need to change teh way we evaluate P
            P will be determined by many values, not just preferred guests. some ideas include
                how early a guest registered (what to do if this person is in a carpool with someone who registered last minute)
                prefered co-guests
                required co-guests (bc car pools)
                being housed with people from the same scene? Maybe? Ignore that for this iteration. 
                late night tendencies. Does this matter? 
                preferences with which gender they'd like to be housed? This can be ignored. 
            can we ask that people list no more than 4 carpool buddies?
            can we have it so that by the time housing registration closes, people must list their car pools?
                make registration work in such a way that they can edit who their car pool buddies are until the very last minute?
                    either that or make it some grunt work to be done by the housing coordinator before they use our algorithm.
                    we can have it so that when people list who they MUST stay with, they list a reason. 
                        Carpools and girlfriend/boyfriend are good reasons.
                        bc we're friends or want to hang out a lot is not.
            I think we should rearrange the algorithm so that people definitely already have carpools organized. 
                if they bitch about it, we can just say that they changed their plans after housing has been assigned. 
                we have to make them agree to it before they finish updating their registration, e.g. "You know that we will assign housing with carpools the way they are right now, and that we will not take into account carpool changes after housing closes."
                    We can make it so that there is a separate account for housing
                        make the housing coordinator nag the shit out of people the week before housing closes to fill out their housing.
                        send them an email saying "URGENT: We don't have your housing info. FILL IT OUT NOW." 
                So, we have some hard restrictions and some soft restrictions
                    Hard restrictions
                        cats, dogs, smoking, rides
                        required co-guests must stay together so taht we can assign housing based on groups
                    Soft restrictions
                        how early the guest registered
                        preferred co-guests
                        being housed with ppl from teh same scene
                        late night tendencies
                        gender housing tendencies (if they would have needed to stay with people of the same gender, we would have seen that in teh misc. info.)
        
        Would it be a good idea to have the GA take into account splitting carpools to get a higher N?
            what I mean is that we have our set of fixed groups of people who need to be togther
                this could be large groups like a whole scene or smaller groups of friends (about 8 or so) or small carpool groups of 4
            We could split them so that we might need to split a carpool group of 4 into two groups of two so that all four of them can get housed instead of not housing the 4 of them bc they won't fit somewhere. 
        
        change P to be a linear combination of all the soft values
        have diminishing returns for people staying together
            different methods
                per person, 1/(something) for each edge, something can be n**2, 2**n, etc.
                per group, 1/n of the graph. 
        We're going to assume that preferred co-guests and required co-guests are the same 
        
    Less Important
        implement feature where guests cannot be housed with smokers if they don't want to be housed with smokers
        Take into account gender preferences when it comes to calculating P
        Add gender preferences to Host and Guest classes
        Get script working to run island_ga.py on https://cloud.sagemath.com/ 
        Add parsing of actual data to add real hosts and guests instead of using the dummy func
            See how this works with real data
        Refactor each section of the main GA code into functions
        Take into account late night tendencies when it comes to calculating P

Genetic Algorithm for Assigning Housing Spots to Guests for Swing Dancing Events. 

To understand how to use this code, see the usage() function or use "python ga.py -usage" on the commandline. 

Tips and Hacks for Usage:
    
    It might be a good idea to tweak the parameters for population size according to your computer's available processing resources.
    
    It's a good idea to check the visualizations during the running to make sure everything is running as it should. 
    
    It's good to have the number of generations unreasonably high to a point where it won't be complete in the time you need it. This way, you can stop it from running and have the results the algorithm generated up to that point. This avoids having idle time that the algorithm isn't using to find better results. 
        The results only get better as more generations pass since we save a global pareto frontier of the best results we've found so far over all the generations. 
        If you want to continue running the algorithm from a certain point, just take all the ".py" files in the output folder and use that folder to seed the starting generation of a new genetic algorithm run using the "-starting_generation_descriptor_dir" option.
    
    It might be a good idea to seed the starting generation with a maximum matching. You can use "Genome(networkx.maximal_matching(housing_graph))" to generate a genome that uses a maximum matching. Put it in a list called "genomes" and put that into a '.py' file, and the file can be used to seed the starting generation of a new genetic algorithm run via the "-starting_generation_descriptor_dir" option. 
    
    Keep in mind that we want to balance exploration and exploitation to get good performance. 
        If we seek exploration and high diversity, we will explore many of options, but these options may not necessarily be good. This will help us avoid local extrema in our search space but may take a lot of time.
        If we seek exploitation and high quality, we will explore only the options that perform best. This, however, may lead us to get stuck in local extrema. 
    
    Ways we can balance exploration and exploitation for good performance include playing with:
        Population Sizes: Larger population sizes will lead to more diversity, but processing each generation will also take more time.  Progress of the genetic search is saved after each generation is processed, so it might be a good idea to have each generation not take a long time as all time spent processing a generation is wasted if that generation has not completed processing. Smaller population sizes will have lower diversity. 
        Tournament Sizes: Smaller tournament sizes increase diversity. Larger tournament sizes lead to greedier searches. 
        Elite Percent: Having a higher percent of elites can decrease diversity and vice-versa (though to what extent this happens also depends on the tournament size). If there are more elites, it is more likely that they will be chosen for crossover and mutation (the selection for both of these is random selection) and vice-versa. Keep in mind that the impact that the percent of elites has on diversity is affected by the tournament size. 
        Mate Percent: Having a higher mate percent can increase diversity as the parents chosen for the mating is random. However, how diverse the new children will be depends on the number of elites in the population, which is dependent on the elite percent and the tournament size, as a larger percent of elites will lead to a larger probability that they will be chosen as parents to create offspring. However, we should keep in mind that these offspring may not necessarily be as elite as the parents. 
        Mutation Percent: Having a higher mutation percent can increase diversity as the genomes chosen for mutation is random. However, how diverse the mutated genomes will be depends on the number of elites in the population, which is dependent on the elite percent and the tournament size, as a larger percent of elites will lead to a larger probability that they will be chosen to be mutated. However, we should keep in mind that these mutated genomes may not necessarily be as elite as the original unmutated elite genome.
        Island GA: Having many different independently growing populations can lead to diversity as each population will go start in and go in different places in the search space. More independent populations will lead to more diverse results. Having these populations crossover with each other can increase exploitation. This can be done wither probabilistically or deterministically. This is worth considering to increase diversity. The interpopulation crossover on performance is hard to determine, but it does necessarily increase exploitation, which can be helpful to balance out the diversity induced by having independent populations.
        Keep in mind that genetic algorithms are randomized algorithms and that there is a lot of noise in the performance. The amount of noise is impacted by the nature of the problem as well as the parameters of our GA. Thus, a lot of the noise in our results is out of our hands, so it's hard to know what decisions are best without getting a strong understanding of the noise, which we can only gain through studying the results of our genetic algorithm with different inputs and parameter selections run a sufficient number of times (a sufficient number of times is also hard to determine). 
        Keep in mind that exploitation and exploration is not something that is easily measured and that it's hard to measure the impact that they have on the results. Two separate parameters may impact diversity, but those may affect the results in different ways. Simply knowing that diversity is impacted does not say anything about the new population members that are being looked at. Thus, it says nothing about how it impacts the results. We'll have to clearly study the results to really know how the impact of the parameters as we do not get a significant amount of insight about our results simply through knowing how the parameters impact exploration and exploitation. 
    
    The starting generation has a noteable impact on the performance of our genetic algorithm. Whichever direction we go in our search space depends on our starting population/starting point. Different starting generations will be different distances from the global extrema of our search space. Starting closer to global extrema is obviously better, but it is hard to determine where in the search space a starting generation is, where the global extrema are, and how far any pair of points are in the search space or even what metric is best to determine distance. We can really know nothing about how well our starting generation performs as we know very little about our search space (which is why we study it and use genetic algorithms to explore it rather than a more elegant method), but we do know that it has an impact. 
        We can manipulate our starting generation using the "-starting_generation_descriptor_dir" command line option. 
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

START_TIME=time.time()

SAVE_VISUALIZATIONS = True
NUM_GENERATIONS_BEFORE_SAVING_VISUALIZATIONS=1
VISUALIZATION_MIN_X=400
VISUALIZATION_MIN_Y=0
VISUALIZATION_MAX_X=50
VISUALIZATION_MAX_Y=450

POPULATION_SIZE_DEFAULT_VALUE = 25
GENERATIONS_DEFAULT_VALUE = 5000
TOURNAMENT_SIZE_DEFAULT_VALUE = 32
ELITE_PERCENT_DFAULT_VALUE = 80
MATE_PERCENT_DEFAULT_VALUE = 10
MUTATION_PERCENT_DEFAULT_VALUE = 10
STARTING_GENERATION_DESCRIPTOR_DIR_DEFAULT_VALUE = '.'
OUTPUT_DIR_DEFAULT_VALUE = './output'

housing_graph = None
hosts = [] 
guests = []

def initialize_guest_and_host_data(output_dir):
    global housing_graph, hosts, guests
    
    # Add hosts and guests
    hosts, guests = generate_hosts_and_guests()
    print "Number of Host Spots:", len(hosts)
    print "Number of Guests:", len(guests)
    print 
    
    # Save host and guest data
    with open(join_paths([os.path.abspath(output_dir),'data.py']),'w') as f:
        f.write('hosts='+hosts.__repr__())
        f.write('\n')
        f.write('guests='+guests.__repr__())
    
    # Create Graph
    housing_graph = networkx.DiGraph()
    
    for host in hosts:
        housing_graph.add_node(host.id_num)
    for guest in guests:
        housing_graph.add_node(guest.id_num)
    
    for host in hosts:
        for guest in guests:
            if are_compatible(host, guest):
                housing_graph.add_edge(host.id_num, guest.id_num) # All of the edges should be ordered in (host,guest) ordering

def add_upper_left_text_box(subplot, text):
    subplot.text(x=0.04, y=0.96, s=text, horizontalalignment='left', verticalalignment='top', transform=subplot.transAxes, bbox=dict(boxstyle='round', facecolor='wheat', alpha=1.0))

def get_subplots():
    fig, subplot = matplotlib.pyplot.subplots()
    subplot.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    subplot.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    subplot.grid(True, which='major', linestyle='-', alpha=0.4)
    subplot.grid(True, which='minor', linestyle='-', alpha=0.2)
    subplot.set_xlabel('N Values')
    subplot.set_ylabel('P Values')
    subplot.set_xlim(left=VISUALIZATION_MIN_X, right=VISUALIZATION_MAX_X)
    subplot.set_ylim(bottom=VISUALIZATION_MIN_Y, top=VISUALIZATION_MAX_Y)
#    subplot.invert_xaxis()
#    subplot.invert_yaxis()
    return fig, subplot

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
        self.late_night_tendencies=late_night_tendencies0 # is a string, one of "early sleeper", "some late night", or "survivors' club".
        self.preferred_house_guests=preferred_house_guests0
        self.misc_info=misc_info0 # is a string
        self.id_num=id_num0 if id_num0!=-1 else generate_unique_identifier()
        assertion(len(self.days_housing_is_available)>0, 'Hosts must have at least one day of housing available.')
    
    def get_clone(self):
        clone = copy.deepcopy(self)
        clone.id_num = -1
        return clone
    
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

def generate_hosts_and_guests(input_xlsx='Expanded_Housing_Data.xlsx', index_of_sheet_containing_data=0):
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
        if initial_edges==[]: 
            # This is a weird hack, but it's necessary bc I suspect there's a bug in the compiler (either that or I'm doing something really funky that I don't realize that's making pointers get all crazy and cause all Genomes initialized with initial_edges=[] to have the same edges). 
            self.chosen_edges=[]
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

def ga(population_size=POPULATION_SIZE_DEFAULT_VALUE, generations=GENERATIONS_DEFAULT_VALUE, tournament_size=TOURNAMENT_SIZE_DEFAULT_VALUE, elite_percent=ELITE_PERCENT_DFAULT_VALUE, mate_percent=MATE_PERCENT_DEFAULT_VALUE, mutation_percent=MUTATION_PERCENT_DEFAULT_VALUE,starting_generation_descriptor_dir=STARTING_GENERATION_DESCRIPTOR_DIR_DEFAULT_VALUE,output_dir=OUTPUT_DIR_DEFAULT_VALUE): 
    
    global SAVE_VISUALIZATIONS
    
    global_pareto_frontier = [] # Dummy initial object so that we don't have to check if it's empty every time we attempt to add something to it. 
    
    # Genetic algorithm
    starter_genomes_and_scores=[] # Get genomes from descriptor files
    for potential_genome_list_descriptor_files in filter(lambda x:'.py'==x[-3:], list_dir_abs(starting_generation_descriptor_dir)):
        lines=open(potential_genome_list_descriptor_files,'r').readlines()
        for line in lines:
            if 'genomes=[Genome([(' == line[:18]: # Not very secure :/ 
                d = dict()
                exec line in globals(), d
                starter_genomes_and_scores += [(genome, 1/(genome.get_N_value()+1), 1/(genome.get_P_value()+1)) for genome in d['genomes']]
    starter_genomes_and_scores = sorted(starter_genomes_and_scores, key=lambda x:(x[0],-x[1])) 
    genomes = []
    prev_inverse_P=inf # We're only starting with the pareto frontier of all the starter genomes bc there are usually too many starter genomes
    for (genome, inverse_N, inverse_P) in starter_genomes_and_scores:
        if inverse_P<=prev_inverse_P:
            genomes.append(genome)
            prev_P = P
    while len(genomes)<population_size:
        genomes.append(Genome())
    
    num_elites = int(round(elite_percent*population_size))
    num_offspring = int(round(mate_percent*population_size))
    num_mutated = int(round(mutation_percent*population_size))
    
    if SAVE_VISUALIZATIONS:
        makedirs(join_paths([output_dir,'all_generations_point_cloud_graph_graph']))
        makedirs(join_paths([output_dir,'point_cloud_graph']))
        makedirs(join_paths([output_dir,'pareto_curve_graph']))
        makedirs(join_paths([output_dir,'global_pareto_curve_graph']))
        makedirs(join_paths([output_dir,'global_pareto_frontier_scores_csv']))
        makedirs(join_paths([output_dir,'all_scores_per_generation_csv']))
        makedirs(join_paths([output_dir,'pareto_frontier_scores_per_generation_csv']))
        makedirs(join_paths([output_dir,'population_data']))
        fig_all_points, subplot_all_points = get_subplots()
        fig_global_pareto_curve_graph, subplot_global_pareto_curve_graph = get_subplots()
    for generation in xrange(generations):
        SAVE_VISUALIZATIONS=(generation%NUM_GENERATIONS_BEFORE_SAVING_VISUALIZATIONS==0)
        print "%-30s Elapsed Time: %015f" % ("Working on generation "+str(generation)+'.',time.time()-START_TIME)
        
        # Save the population
        with open(join_paths([os.path.abspath(output_dir),'population_data','generation_%03d.py'%generation]),'w') as f:
            f.write('genomes='+genomes.__repr__())
        
        # Evaluate each population member
        inverse_N_P_scores = sorted([(index, 1.0/(1+genome.get_N_value()), 1.0/(1+genome.get_P_value())) for index,genome in enumerate(genomes)], key=lambda x:x[1]) # sorted from lowest to highest 1/N values
        xy = sorted(list(set([e[1:3] for e in inverse_N_P_scores])),key=lambda e:(e[0],-e[1]))
        x = [1.0/e[0]-1 for e in xy] # N values
        y = [1.0/e[1]-1 for e in xy] # P values
        with open(join_paths([os.path.abspath(output_dir),'all_scores_per_generation_csv','generation_%03d.csv'%generation]),'w') as f:
            f.write('N, P\n')
            for n,p in zip(x,y):
                f.write(str(int(n))+', '+str(int(p))+'\n')
        if SAVE_VISUALIZATIONS:
            #Save point clouds over all generations visualization
            subplot_all_points.set_title('Generation '+str(generation))
            subplot_all_points.scatter(x, y, zorder=10, c='c', alpha=0.10)
            fig_all_points.savefig(join_paths([output_dir,'all_generations_point_cloud_graph_graph','generation_%03d.png'%generation]))
            # Save only this generation point cloud visualization
            fig, subplot = get_subplots()
            subplot.scatter(x, y, zorder=10, c='r', alpha=1.0)
            fig.savefig(join_paths([output_dir,'point_cloud_graph','generation_%03d.png'%generation]))
            matplotlib.pyplot.close(fig)
        # Get pareto ranking by N and P values
        pareto_ranking = [] 
        if SAVE_VISUALIZATIONS:
            fig_pareto_curve_graph, subplot_pareto_curve_graph = get_subplots()
        for pareto_rank_score in xrange(len(inverse_N_P_scores)): # the number of pareto rank values is upper bounded by the number of points as they all may fall on different pareto curves (imagine if they all lied on the f(x)=x line). 
            indices_to_pop=[]
            prev_inverse_P_score = inf
            for i,(index_of_genome, inverse_N_score, inverse_P_score) in enumerate(sorted(inverse_N_P_scores, key=lambda e:e[1])):
                if inverse_P_score<=prev_inverse_P_score:
                    prev_inverse_P_score=inverse_P_score
                    indices_to_pop.append(i)
                    pareto_ranking.append((index_of_genome, pareto_rank_score, inverse_N_score, inverse_P_score))
            # Update global_pareto_frontier
            if pareto_rank_score==0:
                if SAVE_VISUALIZATIONS:
                    n_of_max_N=int(1.0/pareto_ranking[0][-2]-1)
                    p_of_max_N=int(1.0/pareto_ranking[0][-1]-1)
                    n_of_max_P=int(1.0/pareto_ranking[-1][-2]-1)
                    p_of_max_P=int(1.0/pareto_ranking[-1][-1]-1)
                    add_upper_left_text_box(subplot_pareto_curve_graph, "Max N: (N:"+str(n_of_max_N)+",P:"+str(p_of_max_N)+")\nMax P: (N:"+str(n_of_max_P)+",P:"+str(p_of_max_P)+")")
                new_global_pareto_frontier=sorted(pareto_ranking+global_pareto_frontier, key=lambda x:(x[-2],-x[-1]))
                indices_to_avoid=[]
                prev_inverse_P = inf
                for i, elem in enumerate(new_global_pareto_frontier):
                    inverse_P_score=elem[-1]
                    if inverse_P_score <= prev_inverse_P:
                        prev_inverse_P = inverse_P_score
                        continue
                    indices_to_avoid.append(i)
                for i in indices_to_avoid[::-1]:
                    new_global_pareto_frontier.pop(i)
                global_pareto_frontier=[]
                for i, elem in enumerate(new_global_pareto_frontier):
                    inverse_N_score=elem[-2]
                    inverse_P_score=elem[-1]
                    genome = genomes[elem[0]] if type(elem[0])==int else elem[0]
                    assertion(isinstance(genome,Genome),"genome is not an instance of the class Genome.")
                    global_pareto_frontier.append((genome,inverse_N_score,inverse_P_score))
                with open(join_paths([os.path.abspath(output_dir),'pareto_frontier_scores_per_generation_csv','pareto_frontier_at_generation_%03d.csv'%generation]),'w') as f:
                    f.write('N, P\n')
                    for (_, _, inverse_N_score, inverse_P_score) in pareto_ranking:
                        n = 1.0/inverse_N_score-1
                        p = 1.0/inverse_P_score-1
                        f.write(str(int(n))+', '+str(int(p))+'\n')
            if SAVE_VISUALIZATIONS:
                subplot_global_pareto_curve_graph.set_title('Generation '+str(generation))
                xy = sorted(list(set([(inverse_N_score,inverse_P_score) for (genome,inverse_N_score,inverse_P_score) in global_pareto_frontier])), key=lambda e:(e[0],-e[1]))
                x = [int(1.0/e[0]-1) for e in xy] # N values
                y = [int(1.0/e[1]-1) for e in xy] # P values
                color=numpy.random.rand(3,1)
                subplot_global_pareto_curve_graph.plot(x, y, zorder=10, c=color, alpha=1.0)
                subplot_global_pareto_curve_graph.scatter(x, y, zorder=10, c=color, alpha=1.0)
                add_upper_left_text_box(subplot_global_pareto_curve_graph, "Max N: (N:"+str(x[0])+",P:"+str(y[0])+")\nMax P: (N:"+str(x[-1])+",P:"+str(y[-1])+")")
                fig_global_pareto_curve_graph.savefig(join_paths([output_dir,'global_pareto_curve_graph','generation_%03d.png'%generation]))
                subplot_pareto_curve_graph.set_title('Generation '+str(generation))
                xy = sorted(list(set([inverse_N_P_scores[i][1:3] for i in indices_to_pop])), key=lambda e:(e[0],-e[1]))
                x = [1.0/e[0]-1 for e in xy] # N values
                y = [1.0/e[1]-1 for e in xy] # P values
                color=numpy.random.rand(3,1)
                subplot_pareto_curve_graph.plot(x, y, zorder=10, c=color, alpha=1.0)
                subplot_pareto_curve_graph.scatter(x, y, zorder=10, c=color, alpha=1.0) # points may overlap, and thus some differen colored points may appear on multiple lines, which gives the illusion that the coloring of the points and lines are different.
            for i in indices_to_pop[::-1]:
                inverse_N_P_scores.pop(i)
            if len(inverse_N_P_scores)==0:
                break
        if SAVE_VISUALIZATIONS:
            fig_pareto_curve_graph.savefig(join_paths([output_dir,'pareto_curve_graph','generation_%03d.png'%generation]))
            matplotlib.pyplot.close(fig_pareto_curve_graph)
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
        # Save global_pareto_frontier
        with open(join_paths([os.path.abspath(output_dir),'global_pareto_frontier.py']),'w') as f:
            # We want to save this on every generation in case the running stops for any reason ebfore we've reached our final generation.
            f.write('genomes='+([e[0] for e in global_pareto_frontier]).__repr__())
        with open(join_paths([os.path.abspath(output_dir),'global_pareto_frontier_scores_csv','global_pareto_frontier_at_generation_%03d.csv'%generation]),'w') as f:
            f.write('N, P\n')
            for (_,inverse_n,inverse_p) in global_pareto_frontier:
                f.write(str(int(1.0/inverse_n-1))+', '+str(int(1.0/inverse_p-1))+'\n')
    
    if SAVE_VISUALIZATIONS:
        matplotlib.pyplot.close(fig_all_points)
        matplotlib.pyplot.close(fig_global_pareto_curve_graph)

def usage(): 
    # Example Usage: python ga.py -population_size 100 -generations 100 -output_dir ./output
    print >> sys.stderr, 'python '+__file__+' <options>'
    print >> sys.stderr, ''
    print >> sys.stderr, 'Options:'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -population_size <int>'
    print >> sys.stderr, '        Number of genomes per generation. Default value is '+str(POPULATION_SIZE_DEFAULT_VALUE)+'.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -generations <int>'
    print >> sys.stderr, '        Number of generations. Default value is '+str(GENERATIONS_DEFAULT_VALUE)+'.'
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
    print >> sys.stderr, '    -starting_generation_descriptor_dir <string>'
    print >> sys.stderr, '        Directory containing \'.py\' files that contain lists of Genome objects to be used as the starting point for this genetic search. Default value is '+STARTING_GENERATION_DESCRIPTOR_DIR_DEFAULT_VALUE+'.'
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
    generations = int(get_command_line_param_val_default_value(sys.argv, '-generations', GENERATIONS_DEFAULT_VALUE))
    tournament_size = int(get_command_line_param_val_default_value(sys.argv, '-tournament_size', TOURNAMENT_SIZE_DEFAULT_VALUE))
    elite_percent = float(get_command_line_param_val_default_value(sys.argv, '-elite_percent', ELITE_PERCENT_DFAULT_VALUE))/100.0
    mate_percent = float(get_command_line_param_val_default_value(sys.argv, '-mate_percent', MATE_PERCENT_DEFAULT_VALUE))/100.0
    mutation_percent = float(get_command_line_param_val_default_value(sys.argv, '-mutation_percent', MUTATION_PERCENT_DEFAULT_VALUE))/100.0
    assertion(elite_percent+mate_percent+mutation_percent==1.0,"Sum of elite_percent, mate_percent, and mutation_percent is not equal to 100%.")
    starting_generation_descriptor_dir = os.path.abspath(get_command_line_param_val_default_value(sys.argv, '-starting_generation_descriptor_dir', STARTING_GENERATION_DESCRIPTOR_DIR_DEFAULT_VALUE))
    output_dir = os.path.abspath(get_command_line_param_val_default_value(sys.argv, '-output_dir', OUTPUT_DIR_DEFAULT_VALUE))
    makedirs(output_dir)
    
    print "GA Parameters"
    print "    population_size:", population_size
    print "    generations:", generations
    print "    tournament_size:", tournament_size
    print "    elite_percent: %.2f%%" % (100*elite_percent)
    print "    mate_percent: %.2f%%" % (100*mate_percent)
    print "    mutation_percent: %.2f%%" % (100*mutation_percent)
    print "    starting_generation_descriptor_dir:", starting_generation_descriptor_dir
    print "    output_dir:", output_dir
    print 
    
    initialize_guest_and_host_data(output_dir)
    
    ga(population_size,generations,tournament_size,elite_percent,mate_percent,mutation_percent,starting_generation_descriptor_dir,output_dir)
    
    print 
    print 'Total Run Time: '+str(time.time()-START_TIME)
    print 

if __name__ == '__main__':
    main()

