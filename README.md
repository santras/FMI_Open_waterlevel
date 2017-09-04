Read me get_fmi_open.py

Purpose of code is to retrieve FMI Open Data sea level measurements.The service is provided by Finnish Meteorological Institute and you can view their product descriptions, lincences etc https://en.ilmatieteenlaitos.fi/open-data. This is where you also need to register in order to get a API key needed for this code to work. Save your api key as a FMI_OpenData_Key.txt before running the program.
The FMI Open Data service have some restriction on how much you can download at a time.

Usage:

get_fmi_open_waterlev start_time end_time output_folder_name

Usage Example: python get_fmi_sealevels.py 2001 01 01 2001 01 01 FMIdata > retrieve_info.txt

Program written by Sanna Särkikoski 30.8.2017 with Python 3.6.1, updated 4.9.2017.Notice: Some firewalls (company, government) may be blocking the download with get from requests so if you repeatedly have problems, you may need to check if you can download normally for example using your home connection. 


The data is available (4.9.2017 situation) from 1.1.1971 to a present day exempt from Porvoo Emäsalo station which has started it's operation 2014.FMI has longer time series (oldest 1887), but they are not (yet) available for open data download.   The measurements are quality controlled by FMI first with automatic routines and then later by a person. The sealevels are recorded hourly and given as cm in relation to a yearly theoretical average waterlevel (teoreettinen keskivesi) by each station. More information about theoretical average waterlevel is available http://ilmatieteenlaitos.fi/keskivesitaulukot. Contact information for FMI waterlevel service : vedenkorkeus@fmi.fi.The service have some restriction on how much you can download at a time. Retrieving in a loop like in this code 7 days at a time, seemed to work just fine. I was able to retrieve ~10 years in one go and then pause for a while ~15 -20 min and then I was able to download more.


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
