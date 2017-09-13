#!/usr/bin/env python
# coding: utf-8

# Purpose of this code is to change all the Finnish SeaLevel Values into the NN2000
# from the Mean Sea Level (Keskivesi) they were when downloaded.



def get_names():
    # Get filenames from a file foldername, naming of the variable could be more accurate
    file_n=open('foldernames','r')
    names=(file_n.readlines())
    name=[]
    for ind in range(len(names)):
        name.append((names[ind].strip()))
    return name

def open_rfile(file_name):
    # Open a readable file
    try:
        file=open(file_name,'r')
        data=file.readlines()
        file.close()
        ok=True
    except:
        print("File {} couldn't be opened".format(file_name))
        ok=False
        data=[]
        return data,ok
    return data,ok

def get_var(strings):
    # Takes variables from the string that contains the whole file data
    station=((strings[0].split())[1])
    lat=((strings[1].split())[1])
    lon=((strings[2].split())[1])
    date=[]
    time=[]
    slev=[]
    for ind in range(4,len(strings)):
        date.append(((strings[ind].split())[0]))
        time.append(((strings[ind].split())[1]))
        slev.append(float(((strings[ind].split())[2])))
    return station,lat,lon,date,time,slev



def check_station(name):
    # Matching the names of the stations to the corresponding column in the file for the conversion
    if name=='Kemi':
        ind=0
    elif name=='Oulu':
        ind=1
    elif name=='Raahe':
        ind=2
    elif name=='Pietarsaari':
        ind=3
    elif name=='Vaasa':
        ind=4
    elif name=='Kaskinen':
        ind=5
    elif name=='Pori' or name=='Mäntyluoto' or name=='Mantyluoto':
        ind=6
    elif name=='Rauma':
        ind=7
    elif name=='Turku':
        ind=8
    elif name=='Föglö' or name=='Foglo' or name=='Degerby' or name=='FÃ¶glÃ¶':
        ind=9
    elif name=='Hanko':
        ind=10
    elif name=='Helsinki':
        ind=11
    elif name=='Porvoo':
        ind=12
    elif name=='Hamina':
        ind=13
    else:
        print("Couln't find station"+name)
        return []
    return ind

def add_conversion(station,date,slev):
    # Opens the file for conversions and searches the matching one
    year=[]
    for ind in range(len(date)):
        year.append('y_'+((date[ind])[0:4]))
    f_name='.\Suomi\Meanwater_1931_2017_N2000.txt'
    (con_str,ok)=open_rfile(f_name)
    if not ok:
        exit("Can't do more, need the conversion table to NN2000")
    stationlist=(con_str[0]).split()
    con_year=[]
    con_table=[]
    new_slev=[]
    for inde in range(1,len(con_str)):
        con_year.append(((con_str[inde].split())[0]))
        con_table.append(((con_str[inde].split())[1:]))
    sta_ind=check_station(station)
    for index in range(len(date)):
        for index2 in range(len(con_year)):
            if year[index]==con_year[index2]:
                new_slev.append(slev[index]+(float(con_table[index2][sta_ind])))
    return(new_slev)

def write_newfiles(name,strings,station,date,time,slev):
    # Writes the new file
    file=open(name,'w')
    file.writelines(strings)
    for ind in range(len(date)):
        helper=('{}\t{}\t{}\n'.format(date[ind],time[ind],slev[ind]))
        file.write(helper)
    file.close()

def read_write(mareo,folder):
    #Takes up mareograf at a time, reads the data, converts it and then writes the new file
    path = '.\Suomi\\'
    name = path + folder + mareo
    name2 =path + folder +'New_'+mareo
    (datastring,okey)=open_rfile(name)
    if okey==False:
        return
    (station,lat,lon,date,time,slev)=get_var(datastring)
    new_slev=add_conversion(station,date,slev)
    write_newfiles(name2,datastring[0:4],station,date,time,new_slev)

def main ():
    #Here mainly just ordering the work a folder and mareograph at a time
    foldertlist = ("FMIdata1971_1979\\", 'FMIdata1980_1989\\', 'FMIdata1990_1999\\', 'FMIdata2000_2009\\','FMIdata2010_2017\\')
    mareo_name=get_names()
    ind=0
    for folder in foldertlist:
        ind=ind+1
        for ind in range(len(mareo_name)):
            read_write(mareo_name[ind],folder)
    print('Main of fin_MSL_to_NN2000')

if __name__ == '__main__':
    main()



