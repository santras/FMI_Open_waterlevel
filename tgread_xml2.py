#!/usr/bin/env python
#Contains functions filexml_to_txt(file_name) and xml_to_txt(data). Writes outputfiles with station name as
# the txt file name.
import os

def filexml_to_txt(file_name):
    #Function takes file name and opens it up, output path is assumed to be where program is run and output folder Data.
    kk = open(file_name, 'r')
    xml_to_txt(kk,("Data"))
    return;

def xml_to_txt(data, folder_path=None):
    asi=0
    if folder_path==None:
        folder_path=[]
        asi=1
    else:
        folder_make(folder_path)

    #Funtion takes .xml file and parses it to .txt files. The output txt files names are the mareograph names from the
    # input .xml file. This code works for FMI OPEN DATA Sea Level data. It's only tested with all mareographs, should
    # later be checked also if works if only some mareopgraphs are chose.
    for ll in data:
        lll = ll.strip().split('>')
        if '<gml:name>' in ll:
            name= lll[1].split()[0]
            #outfile=open(name+'.testfile','w')
            #outfile=open(+name+'.txt','w')
            if asi==1:
                dummy_name="{}.txt".format(name)
            else:
                dummy_name="{}\{}.txt".format(folder_path,name)
            print(dummy_name)
            outfile=open(dummy_name,'w')
            outfile.write('Station '+name+'\n')
        if  '<gml:pos>' in ll:
            lat=lll[1].split()[0]
            lon=lll[1].split()[1]
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
    return ;

def folder_make(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    return;


#filexml_to_txt('w_lev_test.xml')
