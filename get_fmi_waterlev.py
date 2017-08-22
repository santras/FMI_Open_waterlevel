#!/usr/bin/env python

# Purpose of code is to retrieve FMI Open Data sea level measurements. The service is provided by Finnish
# Meteorological Institute and you can view their product descriptions, lincences etc
# https://en.ilmatieteenlaitos.fi/open-data. This is where you also need to register in order to get a API key
# needed for this code to work. The service restricts how much you can retrieve data at a single time, in 5 minutes and how much
# you can retrieve with single key within one day.
# Instruction on how to use the code (will someday be)HERE
# get_fmi_waterlev start end
# Program written by Sanna Särkikoski 21.8.2017
# Partly copied from Olli Wilkmans similar code for retrieving temperature observations:
# https://github.com/dronir/PythonClass/blob/master/FMI%20open%20data%20API%20example.ipynb

# This is a crude first version... will be made prettier later and hopefully more easy to use
# Need to actually test the limitations 7 days at a time, 25 days in 5 min, ~2 years a day

import sys
import datetime
from urllib import request
import xml.etree.ElementTree as ET

def get_time_interval():
    # At the moment only with user input, exits if wrong
    # In future: resume from last asignment, 5 min break possibility??
    # User input option
    d_start=[int(i) for i in (sys.argv[1:4])]
    d_end=  [int(i) for i in (sys.argv[4:7])]

    date_s=datetime.date(d_start[0],d_start[1],d_start[2])  # Needs to be individual numbers, can't be a list
    date_e=datetime.date(d_end[0],d_end[1],d_end[2])
    return date_s, date_e;

def check_time_interval(d_start, d_end):
    # Checking that the time interval makes sense and is okey for data retrieval restrictions
    if d_start>d_end:
        little_help=d_end
        d_end=d_start
        d_start=little_help
    if d_start > (datetime.date.today()):        ######## Here maybe ask again the dates?
        print('Genius is eternal patience - Michelangelo')
        print("Let's leave some research for the days to come.")
        exit()
    if d_start<datetime.date(1997,1,1):
        print('Data only available from 1971')
        exit()
    if (d_end - d_start) > (datetime.timedelta(days=25)):  ###### How to wait 5 minutes???
        print('Only 25 days at a time at the moment, please!')
        exit()
    if (d_end-d_start)>(datetime.timedelta(days=830)):                 ###### Come back tomorrow??? Storing of dates?
        print('You can also search for 830 days (~2 years) of data in a day.') # Makes sense if one above will be moved
        exit()
    print('Searching from {} to {}. '.format(d_start, d_end))
    return d_start, d_end;

def make_message(times):
    start_time='{}T00:00:00Z'.format(times[0])
    end_time='{}T00:00:00Z'.format(times[1])
    API_key = open("FMI_OpenData_Key.txt","r").read().strip()

    message =   'http://data.fmi.fi/fmi-apikey/{}/wfs?request=getFeature&storedquery_id=fmi::observations::mareograph' \
                '::timevaluepair&starttime={}&endtime={}'.format(API_key,start_time,end_time)
    return message;

def retrieve_data(message,date_inter):                  # Jokin tässä ei toimi vaikka printed message on ok
    XMLdata = request.urlopen(message).read()
    XMLTree = ET.fromstring(XMLdata)
    #print(message)

    return;

date_start= get_time_interval()[0]
date_end=   get_time_interval()[1]                  # Dates can change order, that's why changed names, I know clumsy..
date_inter=check_time_interval(date_start, date_end)
fmi_message=make_message(date_inter)
print(fmi_message)
retrieve_data(fmi_message, date_inter)

time_lim=datetime.timedelta(days=7)

# while (date_end-date_start)>=time_lim:                    # Opend Data can be searched only 1 week at the time
#     if (date_end-date_start)==time_lim:
#         #print('Searching from {} to {}. '.format(date_start,date_end))
#         date_end = date_end-time_lim
#     else:
#         date_search=(date_end-time_lim)
#         #print('Searching from {} to {}. '.format(date_search, date_end))
#         date_end=date_search
#
#


