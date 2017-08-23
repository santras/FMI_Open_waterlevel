#!/usr/bin/env python

def xml_to_txt(file_name):
    #Funtion takes .xml file and parses it to .txt files. The output txt files names are the mareograph names from the 
    # input .xml file. This code works for FMI OPEN DATA Sea Level data. It's only tested with all mareographs, should 
    # later be checked also if works if only some mareopgraphs are chose. 
    
    kk=open(file_name,'r')
    for ll in kk:
        lll = ll.strip().split('>')
        if '<gml:name>' in ll:
            name= lll[1].split()[0]
            #outfile=open(name+'.testfile','w')
            outfile=open(name+'.txt','w')
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

xml_to_txt('w_lev_test.xml')
