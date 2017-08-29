#!/usr/bin/env python
# coding: utf-8

# Purpose of code is to retrieve FMI Open Data sea level measurements. The service is provided by Finnish
# Meteorological Institute and you can view their product descriptions, lincences etc
# https://en.ilmatieteenlaitos.fi/open-data. This is where you also need to register in order to get a API key
# needed for this code to work. The service restricts how much you can retrieve data at a single time, in 5 minutes and how much
# you can retrieve with single key within one day.
# Instruction on how to use the code (will someday be)HERE
# get_fmi_open_waterlev start end
# Program written by Sanna Särkikoski 21.8.2017
# Partly copied from Olli Wilkmans similar code for retrieving temperature observations:
# https://github.com/dronir/PythonClass/blob/master/FMI%20open%20data%20API%20example.ipynb

# This is a crude first version... will be made prettier later and hopefully more easy to use
# Need to actually test the limitations 7 days at a time, 25 days in 5 min, ~2 years a day

import sys
import datetime
import argparse
from urllib import request
import xml.etree.ElementTree as ET
from tgread_xml import xml_to_txt

def parseArguments():
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

    return args;

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

def retrieve_data(message):                  # Jokin tässä ei toimi vaikka printed message on ok
    XMLdata = request.urlopen(message).read()
    XMLTree = ET.fromstring(XMLdata)
    print('Retrieve success')

    return XMLTree;

# get_fmi_open.py-to-using-argparse
def main():
    args = parseArguments()
    date_start = datetime.date(args.start_y, args.start_m, args.start_d)
    date_end = datetime.date(args.end_y, args.end_m, args.end_d)
#=======
date_start= get_time_interval()[0]
date_end=   get_time_interval()[1]                  # Dates can change order, that's why changed names, I know clumsy..
# HERE LOOPS FOR RETRIEVAL
date_inter=check_time_interval(date_start, date_end)
fmi_message=make_message(date_inter)
print(fmi_message)
XMLData=retrieve_data(fmi_message)
xml_to_txt(XMLData,'Data')

    # HERE LOOPS FOR RETRIEVAL
    date_inter=check_time_interval(date_start, date_end)
    fmi_message=make_message(date_inter)
    print(fmi_message)
    #XMLData=retrieve_data(fmi_message)
# if os.path.exists('Data'):   # Folder name by user?
#     answer = input(" Folder 'Data' exist and may have files that will be re-written do you want to continue Y/N?")
#     if answer=='No' or aswer=='no' or aswer=='N' or aswer=='n':
#         answer2=input("Would you like to make new folder? Y/N")
#         if answer2=='No' or aswer=='no' or aswer=='N' or aswer=='n':
#             exit()
#         else:
#             aswer
    #xml_to_txt(XMLData,'Data')
    kk = open('w_lev_test.xml', 'r')                # REMOVE THIS::: ONLY TEST
    xml_to_txt(kk, args.folder_name)
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

    # How to video https://www.youtube.com/watch?v=9X0i5yOvR_o on parsing .xml
    return;

# get_fmi_open.py-to-using-argparse
if __name__ == '__main__':
    main()
=======
#Maybe like:
# XMLTree.ET("index.xhtml") <Element 'html' at 0xb77e6fac> # Mitäköhän tekee
# p = tree.find("body/p")

# kk=open('feb1.xml','r')
# for ll in kk:
#     lll = ll.strip().split('>')
#     if '<gml:name>' in ll:
#         name= lll[1].split()[0]
#         #outfile=open(name+'.testfile','w')
#         outfile=open(name+'.txt','w')
#         outfile.write('Station '+name+'\n')
#     if  '<gml:pos>' in ll:
#         lat=lll[1].split()[0]
#         lon=lll[1].split()[1]
#         outfile.write('Latitude '+lat+'\n')
#         outfile.write('Longitude '+lon+'\n')
#         outfile.write('--------------\n')
#     if '<wml2:time>' in ll:
#         date= lll[1][0:10]
#         time=lll[1][11:16]
#         outfile.write(date+' '+time)
#     if 'value' in ll:
#         outfile.write(' '+ lll[1].split('<')[0]+'\n' )
# outfile.close()

# How to video https://www.youtube.com/watch?v=9X0i5yOvR_o on parsing .xml

