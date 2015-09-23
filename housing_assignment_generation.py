#!/usr/bin/python

"""
TODO:
    Implement NetworkX code
    Select an output format
    Do we want to put extra weight if the guest needs no rides and the host cna't give rides so that we can save the hosts who do gives rides for those guests who need rides? same for all the other questions
    add late night tendencies to compatibility
    Would it be a good idea to just assign everyone first and then rearrange them so that more subjective things like coguest preferences and late night tendencies match up?
    matching means a set of edges with no common vertices. this means that one host can only be connected to one guest. we can alleviate this problem by making copies of  host if he can host more than 1 person. 

Automated Housing Assigment Generator for Lindy Hop Events. 

Template Host Form: 
    Editor:         https://docs.google.com/forms/d/1vsCgSXCmx8GtmUu9LO9nJktXWbYXGryXb41KQzcw5TU/edit
    Actual Form:    https://docs.google.com/forms/d/1vsCgSXCmx8GtmUu9LO9nJktXWbYXGryXb41KQzcw5TU/viewform?usp=send_form 
    Results:        https://docs.google.com/spreadsheets/d/1U8KVmalXksCqChxEFMO85n9G--4CKGwsiCgEeGPzNok/

Template Guest Form: 
    Editor:         https://docs.google.com/forms/d/1CsMwTDFhpNw9JbidvLzzc5DIn1w8lZT2uwncA-YPUE8/edit
    Actual Form:    https://docs.google.com/forms/d/1CsMwTDFhpNw9JbidvLzzc5DIn1w8lZT2uwncA-YPUE8/viewform?usp=send_form 
    Results:        https://docs.google.com/spreadsheets/d/1GjMc5xxFvUU_kPti-5yFnJyP8EG2woWZeDLIc6OXbo0/

Keys for host:
    "name"                          (string)        First and last name as a single string.
    "email"                         (string)        Email Address.
    "phone number"                  (int)           Ten digit phone number.
    "days housing is available"     (string list)   List of days housing can be provided. Valid values in list are "friday", "saturday", and "sunday".
    "available spots"               (int)           Number of guests that can be hosted.
    "has cats"                      (boolean)       Whether or not cats will be around during the event.
    "has dogs"                      (boolean)       Whether or not dogs will be around during the event.
    "willing to house smokers"      (boolean)       Whether or not smokers can be hosted.
    "willing to provide rides"      (boolean)       Whether or not rides canbe provided for guests.
    "preferred guests"              (string list)   List of names of people the host wishes to house.
    "late night tendencies"         (string)        Describes how late into the night the host dances. Either "early sleeper", "some late night", or "survivors' club".
    "other information"             (string)        Miscellaneous information.

Keys for guest:
    "name"                          (string)        First and last name as a single string.
    "email"                         (string)        Email Address.
    "phone number"                  (int)           Ten digit phone number.
    "days housing is needed"        (string list)   List of days housing is needed. Valid values in list are "friday", "saturday", and "sunday".
    "allergic to cats"              (boolean)       Whether or not the guest is allergic to cats.
    "allergic to dogs"              (boolean)       Whether or not the guest is allergic to dogs.
    "is a smoker"                   (boolean)       Whether or not the guest smokes.
    "needs host to drive"           (boolean)       Whether or not the guest needs rides from the host.
    "preferred co-guests"           (string list)   List of names of people the guess needs to be housed with.
    "late night tendencies"         (string)        Describes how late into the night the guest dances. Either "early sleeper", "some late night", or "survivors' club".
    "other information"             (string)        Miscellaneous information.

"""

import json
import os
import sys
import pdb
import networkx
from util import *

_UNIVERSAL_COUNTER_ = 0

def get_unique_id_number():
    global _UNIVERSAL_COUNTER_ 
    ans = _UNIVERSAL_COUNTER_
    _UNIVERSAL_COUNTER_ += 1
    return ans

#temporary_data_directory = os.path.abspath(generate_unique_directory_name())

def host_guest_pretty_print(host_guest):
    """Pretty prints a host or a guest"""
    max_key_length = len(max(host_guest.keys(), key=len))
    print '\n'
    for key,val in host_guest.items():
        print ('%'+str(max_key_length)+'s: %s') % (key, val)
    print '\n'

def parse_tsv_file(tsv_file_name):
    tsv_lines = open(tsv_file_name, 'r').readlines()
    keys = [f.strip().lower() for f in tsv_lines[0].split('\t')]
    raw_text_data = tsv_lines[1:]
    obj_list=[]
    for line in raw_text_data:
        data = [f.strip().lower() for f in line.split('\t')]
        obj = dict()
        for key, val in zip(keys,data):
            obj[key] = val
        obj['id'] = get_unique_id_number()
        obj_list.append(obj)
    return keys, obj_list

def determine_compatibility(host, guest):
    ans = 0.0
    # can the host provide rides if the guest needs them?
    if guest['do you need your host to drive you around?'] == 'yes':
        if host['are you willing to provide rides to your guests all weekend?'] == 'no':
            return 0.0
    
    # dog allergies 
    if guest['allergic to dogs?'] == 'yes':
        if host['do you own dogs?'] == 'yes':
            return 0.0
    
    # cat allergies 
    if guest['allergic to cats?'] == 'yes':
        if host['do you own cats?'] == 'yes':
            return 0.0
    
    # smoking 
    if guest['are you a smoker?'] == 'yes':
        if host['are you willing to host smokers?'] == 'no':
            return 0.0
    
    # days available
    
    
    # late night tendencies
    # preferred guests
    
#    return ans
    return 1.0

def usage():
    # Example Usage: python housing_assignment_generation.py ./input/guest_data.tsv ./input/host_data.tsv
    print >> sys.stderr, 'python '+__file__+' guest_data.tsv host_data.tsv'
    sys.exit(1)

def main():
    if len(sys.argv) < 3:
        usage()
    os.system('clear')
    
    guest_data_tsv_file_name = sys.argv[1]
    host_data_tsv_file_name = sys.argv[2]
    
    guest_keys, guest_list = parse_tsv_file(guest_data_tsv_file_name)
    host_keys, host_list = parse_tsv_file(host_data_tsv_file_name)
    
#    host_guest_pretty_print(guest_list[0])
#    host_guest_pretty_print(host_list[0])
    
    graph = networkx.Graph()
    
    for guest in guest_list:
        for host in host_list:
            graph.add_edge(host['id'], guest['id'], weight=determine_compatibility(host,guest))
    
    maximum_weighted_matching = networkx.max_weight_matching(graph)
    
    pdb.set_trace()

if __name__ == '__main__':
    main()

