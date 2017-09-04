#!/usr/bin/env python
# Big part of this code was given to me for use.. I have modifield it somewhat for my own puposes. It is for FMI Open Data
# and spesifically for mareograph observations. At the moment the use is to take a .xml file and then write it to a text file.
# However in the future, idea would be that no saving of .xml file would be needed.

import os

def filexml_to_txt(file_name):
    #Function takes file name and opens it up, output path is assumed to be where program is run and output folder Data.
    kk = open(file_name, 'r')
    xml_to_txt(kk,("Data"))
    return

def check_outfile(name):
    # check if outfile exist or not
    if os.path.exists(name):
        file_exist=False
    else:
        file_exist=True
    return file_exist

def xml_to_txt(data, folder_path=None):
    # Funtion takes .xml file and parses it to .txt files. The output txt files names are the mareograph names from the
    # input .xml file. This code works for FMI OPEN DATA Sea Level data.
    asi=0
    if folder_path==None:
        folder_path=[]
        asi=1
    else:
        folder_make(folder_path)

    for ll in data:
        lll = ll.strip().split('>')
        if '<gml:name>' in ll:
            name= lll[1].split()[0]
            if asi==1:
                dummy_name="{}.txt".format(name)
            else:
                dummy_name="{}\{}.txt".format(folder_path,name)
            # This is added to make sure data is not ovewritten
            is_new_file=check_outfile(dummy_name)
            if (is_new_file):                           # 2 ways of opening, new folder and adding to existing files
                outfile=open(dummy_name,'w')
                outfile.write('Station '+name+'\n')
            else:
                outfile=open(dummy_name,'a+')

        if  '<gml:pos>' in ll:
            lat=lll[1].split()[0]
            lon=lll[1].split()[1]
            if(is_new_file):                            # write only if new file
                outfile.write('Latitude '+lat+'\n')
                outfile.write('Longitude '+lon+'\n')
                outfile.write('--------------\n')
        if '<wml2:time>' in ll:
            date= lll[1][0:10]
            time=lll[1][11:16]
            outfile.write(date+' '+time)
        if 'value' in ll:
            outfile.write(' '+ lll[1].split('<')[0]+'\n' )
    outfile.close()
    return

def folder_make(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    return


#filexml_to_txt('w_lev_test.xml')