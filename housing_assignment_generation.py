#!/usr/bin/python

"""
TODO:
    Implement NetworkX code

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

temporary_data_directory = os.path.abspath(generate_unique_directory_name())

'''
def housing_csv_to_json(guest_data_csv_file_name, host_data_csv_file_name, output_json_file_name):
    guest_csv_lines = open(guest_data_csv_file_name, 'r').readlines()
    keys = [f.strip() for f in csv_lines[0].split(',')]
    raw_text_data = csv_lines[1:]
    guests_list=[]
    for line in raw_text_data:
        guest_data = [f.strip() for f in line.split(',')]
        guest_object = dict()
        for key, val in zip(keys,guest_data):
            guest_object[key] = val
            guests_list.append(guest_object)
    pdb.set_trace()
'''

def usage():
    # Example Usage: python housing_assignment_generation.py ./input/guest_data.csv ./input/host_data.csv housing_assignments.json
    print >> sys.stderr, 'python '+__file__+' guest_data.csv host_data.csv output.json'
    sys.exit(1)

def main():
    if len(sys.argv) < 4:
        usage()
    guest_data_csv_file_name = sys.argv[1]
    host_data_csv_file_name = sys.argv[2]
    output_json_file_name = sys.argv[3]
    
#    guest_data_json_file_name = remove_file_extension(guest_data_csv_file_name)+'.json'
#    host_data_json_file_name = remove_file_extension(host_data_csv_file_name)+'.json'
    
    asd

if __name__ == '__main__':
    main()

