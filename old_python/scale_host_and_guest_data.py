#!/usr/bin/python

import os
import sys
import pdb
import time
import random
import copy
import xlwt
import xlrd
from util import *


def usage(): 
    # Example Usage: python scale_host_and_guest_data.py Sample_Housing_Data.xlsx 400 400 Expanded_Housing_Data.xlsx
    print >> sys.stderr, 'python '+__file__+' input.xlsx new_num_host_spots new_num_guests output.xlsx'
    print >> sys.stderr, ''
    print >> sys.stderr, '    input.xlsx'
    print >> sys.stderr, '        Input file containing host and guest data we want our new expanded set of data to be based on.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    new_num_host_spots'
    print >> sys.stderr, '        The number of host spots to be available. This is different from the number of hosts as a host can house multiple people.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    new_num_guests'
    print >> sys.stderr, '        The number of guests needing to be housed.'
    print >> sys.stderr, ''
    print >> sys.stderr, '    output.xlsx'
    print >> sys.stderr, '        New output file.'
    print >> sys.stderr, ''
    sys.exit(1) 

def main():
    start_time = time.time()
    
    print '\n'*100 # Clear
    
    if len(sys.argv) < 5 or '-usage' in sys.argv: 
        usage()
    
    input_file = os.path.abspath(sys.argv[1])
    new_num_host_spots = int(sys.argv[2])
    new_num_guests = int(sys.argv[3])
    output_file = os.path.abspath(sys.argv[4])
    
    print "Parameters"
    print "    input_file:", input_file
    print "    new_num_host_spots:", new_num_host_spots
    print "    new_num_guests:", new_num_guests
    print "    output_file:", output_file
    print 
    
    input_workbook = xlrd.open_workbook(input_file)
    input_sheet = input_workbook.sheet_by_index(0) # Assuming all relevant data is in the first sheet
    column_names = input_sheet.row_values(0)
    
    is_host_index = column_names.index("Local Housing")
    num_spots_available_index = column_names.index("How Many People Can You House?")
    days_housing_is_available_index = column_names.index("On Which Days Can You Provide Housing?")
    days_housing_is_needed_index = column_names.index("On Which Days Do You Need Housing?")
    
    host_spots = 0
    host_data_lines = []
    guest_data_lines = []
    
    for rownum in xrange(1,input_sheet.nrows):
        line_data = input_sheet.row_values(rownum)
        if line_data[is_host_index]=="I live in Richmond and would be happy to host fellow Lindy Hoppers because I'm awesome!": # This person is a host
            host_data_lines.append(line_data)
        
        elif line_data[is_host_index]=="I will be traveling from out-of-town and would appreciate local housing.": # This person is a guest
            guest_data_lines.append(line_data)
    
    output_workbook = xlwt.Workbook()
    output_sheet = output_workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    
    for col,column_name in enumerate(column_names):
        output_sheet.write(0,col,column_name)
        
    row = 1
    host_number = 1
    while host_spots < new_num_host_spots: # Add hosts
        line_data = random.choice(host_data_lines)
        if not any(["Friday" in line_data[days_housing_is_available_index], "Saturday" in line_data[days_housing_is_available_index], "Sunday" in line_data[days_housing_is_available_index]]):
            continue
        for col,datum in enumerate(line_data):
            output_sheet.write(row,col,datum)
        output_sheet.write(row,0,'Host %03d'%host_number)
        host_spots += max(0,line_data[num_spots_available_index])
        host_number += 1
        row += 1
    
    guest_number = 1
    while guest_number < 1+new_num_guests: # Add guests
        line_data = random.choice(guest_data_lines)
        if not any(["Friday" in line_data[days_housing_is_needed_index], "Saturday" in line_data[days_housing_is_needed_index], "Sunday" in line_data[days_housing_is_needed_index]]):
            continue
        for col,datum in enumerate(line_data):
            output_sheet.write(row,col,datum)
        output_sheet.write(row,0,'Guest %03d'%guest_number)
        guest_number += 1
        row += 1
    
    output_workbook.save(output_file)
    
    print 
    print 'Total Run Time: '+str(time.time()-start_time)
    print 

if __name__ == '__main__':
    main()

