#!/usr/bin/env python
# coding: utf-8

# Purpose of code is to retrieve FMI Open Data sea level measurements. The service is provided by Finnish
# Meteorological Institute and you can view their product descriptions, lincences etc
# https://en.ilmatieteenlaitos.fi/open-data. This is where you also need to register in order to get a API key
# needed for this code to work. The service restricts how much you can retrieve data at a single time, in 5 minutes and how much
# you can retrieve with single key within one day.
# Instruction on how to use the code (will someday be)HERE
# get_fmi_open_waterlev start end output_folder_name
# Program written by Sanna Särkikoski 21.8.2017
# Partly copied from Olli Wilkmans similar code for retrieving temperature observations:
# https://github.com/dronir/PythonClass/blob/master/FMI%20open%20data%20API%20example.ipynb

# This is a crude first version... will be made prettier later and hopefully more easy to use
# Need to actually test the limitations 7 days at a time =TRUE
# Seems to limit ~9 years at a time, maybe test 10 tomorrow or later today
# (25 days in 5 min, ~2 years a day not true)


#  Progress: Code should work okey with less than 7 days time periods, next to get not to override if over 7 days
#  Interestingly the 21 days doesen't seem to be a thing, maybe 2 years could be retrievd at once, if not maybe month at a time then 5 min
#  1 Year seemed to work okey... so did 2 years
#  python get_fmi_sealevels.py 1971 01 01 1979 12 31 FMIdata1971_1979 > retrieve_info.txt
#  NEXT TEST: python get_fmi_sealevels.py 1980 01 01 1989 12 31 FMIdata1980_1989 > retrieve_info2.txt
#  NEXT TEST: python get_fmi_sealevels.py 1990 01 01 1999 12 31 FMIdata1990_1999 > retrieve_info3.txt
#  NEXT TEST: python get_fmi_sealevels.py 2000 01 01 2009 12 31 FMIdata2000_2009 > retrieve_info4.txt
# NEXT TEST: python get_fmi_sealevels.py 2010 01 01 2017 8 30 FMIdata2010_2017 > retrieve_info5.txt
# Next after this, calculate into actual 2000 height from mean water heights and put into one big file?

import argparse
import datetime
#import xml.etree.ElementTree as ET
#from urllib import request
import requests
import os

from tgread_xml import xml_to_txt


def parseArguments():
    # Using argparse to store comman line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("start_y", help="Start year", type=int)
    parser.add_argument("start_m", help="Start month", type=int)
    parser.add_argument("start_d", help="Start day", type=int)

    parser.add_argument("end_y", help="End year", type=int)
    parser.add_argument("end_m", help="End month", type=int)
    parser.add_argument("end_d", help="End day", type=int)

    # Optional arguments
    parser.add_argument("folder_name", help="Folder name for output", default="Data", nargs='?')

    # Print version
    parser.add_argument("--version", action="version", version='%(prog)s - Version 1.0')

    # Parse arguments
    args = parser.parse_args()

    return args

def check_time_interval(d_start, d_end):
    # Checking that the time interval makes sense and is okey for data retrieval restrictions

    if d_start>d_end:   # start date and end date in proper order in command line arguments, if not -> swap
        little_help=d_end
        d_end=d_start
        d_start=little_help
    if d_start > (datetime.date.today()):   # Dates not accidentally in future  #### Improvenment: could be to ask again
        print('Genius is eternal patience - Michelangelo')
        print("Let's leave some research for the days to come.")
        exit()
    if d_start<datetime.date(1971,1,1):  # Data availability
        print('Data only available from 1971')
        exit()
    # if (d_end - d_start) > (datetime.timedelta(days=25)):  # Retrieval restriction doesen't seem to be used
    #     print('Only 25 days at a time at the moment, please!')
    #     exit()
    # if (d_end - d_start)>(datetime.timedelta(days=830)): # Retrieval restriction doesen't seem to be used
    #     print('You can also search for 830 days (~2 years) of data in a day.')
    #     exit()

    print('Searching from {} to {}. '.format(d_start, d_end))

    return d_start, d_end

def check_folder(folder_name):
    if os.path.exists(folder_name):   # Folder name by user?
        answer = input(" Folder allready exist. If outputfiles exist, they will be appended.  Would you like to rethink "
                       "this? (Y = Make a new folder or exit program) ")
        if answer=='Yes' or answer=='yes' or answer=='y' or answer=='Y':
            answer2=input("Would you like to make new folder? Y/N  (N exits program) ")
            if answer2=='No' or answer2=='no' or answer2=='N' or answer2=='n':
                print('Exiting without doing anything.')
                exit()
            else:
                answer3=input('Give new folder_name. ')
                folder_name=answer3
                check_folder(folder_name)
    return folder_name

def make_message(time_s,time_e):
    # Puts together the string to use for data retrieval
    start_time='{}T00:00:00Z'.format(time_s)      ##### Improvement: Input could include time of day as well
    end_time='{}T23:00:00Z'.format(time_e)
    API_key = open("FMI_OpenData_Key.txt","r").read().strip()
    message =   'http://data.fmi.fi/fmi-apikey/{}/wfs?request=getFeature&storedquery_id=fmi::observations::mareograph' \
                '::timevaluepair&starttime={}&endtime={}'.format(API_key,start_time,end_time)

    return message

def retrieve_data(message):
    # Retrieves data from the open data service                 #### Not the most elegant way of doing this.. but should work
    # How to from https://pybit.es/download-xml-file.html
    retreave_ok=True
    try:
        response = requests.get(message)
        with open('feed.xml', 'wb') as file:
            file.write(response.content)
    except:
        print('Retrieve failed')
        retreave_ok=False

    return retreave_ok

def loop_retrievals(date_start,date_end,folder_name):
    question=True
    while (question==True):
        if (date_end+datetime.timedelta(days=1)- date_start) <= (datetime.timedelta(days=7)):
            #print('Searching from {} to {}. '.format(date_start,date_end))
            fmi_message=make_message(date_start,date_end)
            ret_ok=retrieve_data(fmi_message)
            kk = open('feed.xml', 'r')
            xml_to_txt(kk,folder_name)
            kk.close()
            #print('Here 1')
            question=False
        else:
            date_search=(date_start+datetime.timedelta(days=6))
            #print('Searching from {} to {}. '.format(date_start,date_search))
            fmi_message=make_message(date_start,date_search)
            ret_ok=retrieve_data(fmi_message)
            kk = open('feed.xml', 'r')
            xml_to_txt(kk,folder_name)
            kk.close()
            date_start=(date_search+datetime.timedelta(days=1))
            #print('Here 2')
        if ret_ok==False:
                print('Search from {} to {} failed. '.format(date_start,date_end))
def main():
    # Makes the whole thing to be able to be called from another script

    args = parseArguments()
    folder_name_ok=check_folder(args.folder_name)
    date_start0 = datetime.date(args.start_y, args.start_m, args.start_d)   # date_start0 date_end0 untested if okey
    date_end0 = datetime.date(args.end_y, args.end_m, args.end_d)

    # HERE LOOPS FOR RETRIEVAL
    [date_start1,date_end1]=check_time_interval(date_start0, date_end0)
    loop_retrievals(date_start1,date_end1,folder_name_ok)

    return

if __name__ == '__main__':
    main()

