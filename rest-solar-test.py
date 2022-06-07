import requests
import datetime
import  json
from requests.auth import HTTPBasicAuth #Does base encoding
from datetime import timedelta
import sys
import os
#import argparse

def get_observer_location():
    """Returns the longitude and latitude for the location of this machine.
    Returns:
    str: latitude
    str: longitude"""


    url='http://ip-api.com/json/?fields=61439'

    output= requests.get(url) 

    #if output.status_code== 200:
    #    dict_obj = output.content

    data=output.json()
    outdata= data['lat'], data['lon'],data['query']

    return outdata[0], outdata[1]


def get_sun_position(latitude, longitude):
    """Returns the current position of the sun in the sky at the specified location
Parameters:
latitude (str)
longitude (str)
Returns:
float: azimuth
float: altitude
"""


    login= {"applicationId":"", 
            "applicationSecret":""}
    
    login['applicationId'] = sys.argv[1]
    login['applicationSecret'] = sys.argv[2]
     
            
    today = datetime.datetime.now()
    now_date = str(today).split()[0]

    yesterday = today - timedelta(hours = 1)
    yes_date=(str(yesterday).split())[0]
    yes_time = str(yesterday).split()[1][0:8]
    body="saturn" #Planet name

    url = "https://api.astronomyapi.com/api/v2/bodies/positions/"+body
    #use Elrvation as 50 
    querystring = {"latitude":latitude,"longitude":longitude,"from_date":yes_date,"to_date":now_date,"elevation":"50","time":yes_time}
    response = requests.request("GET", url,  params=querystring,  auth=HTTPBasicAuth(login['applicationId'],login['applicationSecret']))
    data_sun= json.loads(response.content)

    sun_loc= data_sun['data']['table']['rows'][0]['cells'][0]['position']['horizonal']

    sun_alt=float(sun_loc['altitude']['degrees'])
    sun_azi=float(sun_loc['azimuth']['degrees'])
    distance = data_sun['data']['table']['rows'][0]['cells'][0]['distance']['fromEarth']['km']
    magnitude = data_sun['data']['table']['rows'][0]['cells'][0]['extraInfo']['magnitude']
    print (f"Distance from earth to {body} is {distance} Km and Magnitude is {magnitude}")

    return sun_alt, sun_azi, body

def print_position(azimuth, altitude,body):
    """Prints the position of the sun in the sky using the supplied coordinates
    Parameters:
    azimuth (float)
    altitude (float)"""
    #body="Sun"
    print(f"The {body} is currently at: azimuth of ** {azimuth}  and altitude of ** {altitude}")

newloc=""

if newloc == "":
    latitude, longitude = get_observer_location()
    azimuth, altitude, body= get_sun_position(latitude, longitude)
else:
    azimuth, altitude, body= get_sun_position(newloc)
print_position(azimuth, altitude,body)
print ("My local machine is  at", latitude, longitude,)