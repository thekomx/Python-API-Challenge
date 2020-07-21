# Function in this module requests API from Openweather https://openweathermap.org/
# Return responsed data in Pandas DataFrame


import pandas as PD
import requests as REQ
import json as JSON
import datetime

from config import api_key_ow as KEY


# --- This function request (yesterday, UTC time) Weather data from Openweather API
# --- return data in DataFrame 
# --- contains 'Temperature','Humidity','Cloudiness','Wind Speed (mph)' and City id from passed DataFrame in column 'index_x'
# --- Cities details DataFrame mast be passed to call
def get_weather(df):
    #- Get date/time and convert to number for API requesting
    today = datetime.datetime.utcnow().date()
    yesterday = today - datetime.timedelta(days=2)
    dt = int(datetime.datetime.utcnow().timestamp())
    #-

    #- Empty tempolary DataFrame for resposed weather details
    #- This DataFrame is the return DataFrame
    temp_df = PD.DataFrame({}, columns=['index_x','Temperature','Humidity','Cloudiness','Wind Speed (mph)'])

    total=succ=fail = 0     #-to store the number of Total, Success, Fail requests
    units='imperial'

    print('Requesting Weather Data From the Source.')
    for series_x in df.itertuples():
        city_country = f'{series_x.City.capitalize()}, {series_x.Country.upper()}'  #-Caption for progressing output
        total+=1
        try:
            url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={series_x.Latitude}&lon={series_x.Longitude}&dt={dt}&units={units}&appid={KEY}'
            req_json = REQ.get(url).json()
            temp_df = temp_df.append({'index_x':series_x[0], 'Temperature':req_json['current']['temp'], 'Humidity':req_json['current']['humidity'], 'Cloudiness':req_json['current']['clouds'], 'Wind Speed (mph)':req_json['current']['wind_speed']*60}, ignore_index=True)
            print(f'{total}. {city_country} weather data received.✔')
            succ+=1
        except:
            print(f'🚨Error getting weather data for {city_country} !!!🚨')
            fail+=1

    print('--------------------------------------------------')
    print(f'Total cities requested : {total}')
    print(f'Success request returned : {succ}')
    print(f'Request Failed : {fail}')
    print('--------------------------------------------------')
    
    return temp_df