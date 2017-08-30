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
# Need to actually test the limitations 7 days at a time, 25 days in 5 min, ~2 years a day

import argparse
import datetime
#import xml.etree.ElementTree as ET
#from urllib import request
import requests

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
    if d_start<datetime.date(1997,1,1):  # Data availability
        print('Data only available from 1971')
        exit()
    if (d_end - d_start) > (datetime.timedelta(days=25)):  # Retrieval restriction #### Improvenment: Wait 5 minutes???
        print('Only 25 days at a time at the moment, please!')
        exit()
    if (d_end - d_start)>(datetime.timedelta(days=830)): # Retrieval restriction   #### Improvement:  Come back tomorrow??? Storing of dates?
        print('You can also search for 830 days (~2 years) of data in a day.')
        exit()

    print('Searching from {} to {}. '.format(d_start, d_end))

    return d_start, d_end

def make_message(times):
    # Puts together the string to use for data retrieval
    start_time='{}T00:00:00Z'.format(times[0])      ##### Improvement: Input could include time of day as well
    end_time='{}T00:00:00Z'.format(times[1])
    API_key = open("FMI_OpenData_Key.txt","r").read().strip()
    message =   'http://data.fmi.fi/fmi-apikey/{}/wfs?request=getFeature&storedquery_id=fmi::observations::mareograph' \
                '::timevaluepair&starttime={}&endtime={}'.format(API_key,start_time,end_time)

    return message

def retrieve_data(message):
    # Retrieves data from the open data service                 #### Not the most elegant way of doing this.. but should work
    # How to from https://pybit.es/download-xml-file.html
    response = requests.get(message)
    with open('feed.xml', 'wb') as file:
        file.write(response.content)

    print('Retrieve success')

    return

def main():
    # Makes the whole thing to be able to be called from another script

    args = parseArguments()
    date_start = datetime.date(args.start_y, args.start_m, args.start_d)
    date_end = datetime.date(args.end_y, args.end_m, args.end_d)

    # HERE LOOPS FOR RETRIEVAL
    date_inter=check_time_interval(date_start, date_end)
    fmi_message=make_message(date_inter)
    #print(fmi_message)
    retrieve_data(fmi_message)
    kk = open('feed.xml', 'r')
    xml_to_txt(kk, args.folder_name)
    kk.close()

        #XMLData=retrieve_data(fmi_message)
        # if os.path.exists('Data'):   # Folder name by user?
        #     answer = input(" Folder 'Data' exist and may have files that will be re-written do you want to continue Y/N?")
        #     if answer=='No' or aswer=='no' or aswer=='N' or aswer=='n':
        #         answer2=input("Would you like to make new folder? Y/N")
        #         if answer2=='No' or aswer=='no' or aswer=='N' or aswer=='n':
        #             exit()
        #         else:
        #             aswer
    #kk = open('testi_data.xml', 'r')                # REMOVE THIS::: ONLY TEST
    #xml_to_txt(kk, args.folder_name)
    #time_lim=datetime.timedelta(days=7)

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

        # How to video https://www.youtube.com/watch?v=9X0i5yOvR_o on parsing .xml
    return

if __name__ == '__main__':
    main()

#Maybe like:
# XMLTree.ET("index.xhtml") <Element 'html' at 0xb77e6fac> # Mitäköhän tekee
# p = tree.find("body/p")
