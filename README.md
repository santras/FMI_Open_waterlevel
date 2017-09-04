Read me get_fmi_open.py

#Purpose of code is to retrieve FMI Open Data sea level measurements. 
The service is provided by Finnish
Meteorological Institute and you can view their product descriptions, lincences etc
https://en.ilmatieteenlaitos.fi/open-data. This is where you also need to register in order to get a API key
needed for this code to work. Save your api key as a FMI_OpenData_Key.txt before running the program.
The FMI Open Data service have some restriction on how much you can download at a time.
Usage:
get_fmi_open_waterlev start_time end_time output_folder_name
Usage Example: python get_fmi_sealevels.py 2001 01 01 2001 01 01 FMIdata > retrieve_info.txt
Program written by Sanna Särkikoski 30.8.2017 with Python 3.6.1, updated 4.9.2017.
Notice: Some firewalls (company, government) may be blocking the download with get from requests so if you repeatedly have problems, 
you may need to check if you can download normally for example using your home connection. 

The data in FMI Open Data Sealevel measurements is tide gauge date from 14 stations:
Kemi Ajos					65.67291 	24.51526 	100539
Raahe Lapaluoto 				64.66590 	24.40708 	100540
Helsinki Kaivopuisto 				60.15363 	24.95622 	132310
Vaasa Vaskiluoto 				63.08150 	21.57118 	134223
Rauma Ulko-Petäjäs 				61.13353 	21.42582 	134224
Turku Ruissalo Saaronniemi 			60.42828 	22.10053 	134225
Oulu Toppila 					65.04030 	25.41820 	134248
Pietarsaari Leppäluoto 				63.70857 	22.68958 	134250
Porvoo Emäsalo					60.20579	25.62509	100669
Kaskinen Ådskär 				62.34395 	21.21483 	134251
Föglö Degerby 					60.03188 	20.38482 	134252
Hanko Pikku Kolalahti 				59.82287 	22.97658 	134253
Hamina Pitäjänsaari 				60.56277 	27.17920 	134254
Pori Mäntyluoto Kallo 				61.59438 	21.46343 	134266

The data is available (4.9.2017 situation) from 1.1.1971 to a present day exempt from Porvoo Emäsalo station which has started it's operation 2014.
FMI has longer time series (oldest 1887), but they are not (yet) available for open data download.  
The measurements are quality controlled by FMI first with automatic routines and then later by a person.
The sealevels are recorded hourly and given as cm in relation to a yearly theoretical average waterlevel (teoreettinen keskivesi) by each station. More information about theoretical average waterlevel 
is available http://ilmatieteenlaitos.fi/keskivesitaulukot. 
Contact information for FMI waterlevel service : vedenkorkeus@fmi.fi.
The service have some restriction on how much you can download at a time. 
Retrieving in a loop like in this code 7 days at a time, seemed to work just fine. I was able to retrieve ~10 years in one go and then pause for a while ~15 -20 min and then I was able to download more.


Other information and possible problematic situations:

The code should be generally run in the directory where you wish the output files to be in. You can give the program a output_folder_name and it creates such a folder into the location you are running the program in. 
Outputfolder name can also be a location like MyData\Data in which case unless MyData allready exists the program will make it.  
If no outputfolder name is given the default name is "Data". Genrally the program is pretty rough code with very limited amount of checks and error handling, but if you give a folder name that is allready made the program  
will ask you if you wish to rethink. If you answer no the program will take existing files with the station names in that folder and append the new information after old information. 
This might create a problem if you are calling this program from another program and you allready have a folder with the desired name.
   
The code needs dates of your desired time interval in a format YYYY MM DD at this time you can only ask full days from 00-23 hours (hourly data) with the exeption of current day, where data received is for the last passed hour.
 
If you don't have the .py file in the directory you are running the program from please note that you may need to write the full path of the program when running it example:
python PATH_TO_PROGRAM\get_fmi_sealevels.py 2001 01 01 2001 01 01 FMIdata > retrieve_info.txt the same might sometimes be necessary for the python as well if you don't have python saved into your path variables.
However in this case you may need to manually insert the path to the file tgread_xml into your python paths. 

The program uses simple get from requests to retrieve the webpage and then saves it to a file called feed.xml, this same file is re-written multiple times, and you can delete it after you have run the code.  




get_fmi_sealevels.py
	imports:
		argparse
		datetime
		requests
		os
	own imports:
		from tgread_xml import xml_to_txt ("xml_to_txt" is a file that reads lines of the .xml file and writes the information into a .txt file.)
	includes modules:
		parseArguments()																		return args=imported_module									
		check_time_interval(d_start=datetime.date, d_end=datetime.date)							return d_start=datetime.date, d_end=datetime.date 
		check_folder(folder_name=string)														return folder_name=string
		make_message(time_s=datetime.date, time_e=datetime.date)								return message=string
		retrieve_data(message=string)															return retreave_ok=boolean
		loop_retrievals(date_start=datetime.date, date_end=datetime.date, folder_name=string)
		main()
	Other needed:
		FMI_OpenData_Key.txt (The FMI Open Data Key saved as FMI_OpenData_Key.txt)


Big part of this code was given to me for use.. I have modifield it somewhat for my own puposes. It is for FMI Open Data
and spesifically for mareograph observations. At the moment the use is to take a .xml file and then write it to a text file.
However in the future, idea would be that no saving of .xml file would be needed.		
		
tgread_xml.py
	imports:
		os
	includes modules:
		filexml_to_txt(file_name=string) NOT IN USE
		check_outfile(name=string)																return file_exist=Boolean
		xml_to_txt(data=string, folder_path=None=PATH)
		folder_make(folder=string)


Thank you for Olli Wilkman for giving his example https://github.com/dronir/PythonClass/blob/master/FMI%20open%20data%20API%20example.ipynb 
I also thank the person writing the original "parsing" script I used for the tgread_xml.py

Possible Future improvements:
Test if output file can be in completely different location.. with just givin it's path as the folder name
How to run if programs files are in a different location...importing tgread_xml
Possibility of re-writing the files instead of appending?
Error handlings -what if time is not given
Calling the program from another program -- what if folder allready exists?
Date + TIME input
Fetch only sertain stations
To actually do parsing directly instead of saving to a file first
Other error handlings

Can the script be modified for other uses as well, for example other data in fmi open?
