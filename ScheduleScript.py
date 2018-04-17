import requests
import schedule
import time
import datetime as d

timeout = time.time() + 60*14400 #minutes


def job():
    """Collecting weather data from National Weather Service for a particular location using its Latitude/Longitude
    This data is in the form of XML
    This code is collecting temperature in every 60 minutes . Collection of Data continues for 10 days"""


    print("Creating File....")
    weatherXML = requests.get("https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=37.35&lon=-122.14&product=time-series&temp=temp&maxt=maxt&mint=mint").text
    str_ts = d.datetime.strftime(d.datetime.now(), '%Y-%m-%d %H-%M-%S')
    output_file_name = str_ts		#Setting the name of file to current date and time so every file will be unique
    print output_file_name
    f = open(output_file_name, "w")
    f.write(weatherXML)
    f.close()

schedule.every(180).minutes.do(job)		# In Every 60 minutes the code will Execute

while True:
    schedule.run_pending()
    if time.time() > timeout:		# After 24000 minutes the program will stop Automatically
        break
        # time.sleep(1)