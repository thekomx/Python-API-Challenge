# Functions in this module return a random city in Pandas DataFrame
# The DataFrame contains columns - 'Latitude', 'Longitude', 'City', 'Country'(short form)
# The world cities database is from CitiPy package https://pypi.org/project/citipy/

import os as OS
import csv as CSV
import pandas as PD

# - Initialize when modole is imported
file_path = OS.path.join('..','Resources','Data','WorldCities.csv')
with open(file_path, 'r') as csv_file:
    citipy_df = PD.DataFrame(CSV.reader(csv_file, delimiter=','))
    citipy_df.columns = citipy_df.loc[0]
    citipy_df = citipy_df.drop(index=0)
    citipy_df['Latitude'] = citipy_df['Latitude'].astype(float)
    citipy_df['Longitude'] = citipy_df['Longitude'].astype(float)
# -

# -- This function returns a random city in DataFrame
# -- default return 5 cities
# -- returns empty DataFrame when 0 or less is passed
def random_cities(n=5):
    if n <= 0:
        return_df = PD.DataFrame({})
    else:
        return_df = citypy_df.sample(n)
    
    return return_df
# --


# --- This function returns 611(approx.)
# --- sample randomly spread (quite fairly equally) between Latitude lines (regardless of Longitude)
# --- randomly pick cities for every 5 latitude lines. (0-4, 5-9, 10-14 ...)
# --- Northen Hem. gets ~27 cities, Southern Hem gets ~20 cities every 5 Latitude steps
# --- Northen Hem. from 0-80° (there is no city above this latitude)
# --- Southern Hem. from 0-60° (There is no city below this Latitude)
# --- random will result 2/3 of cities fron Northen Hem. 1/3 From the Southern Hem.
# --- this due to only about 1/3 of the earth land in the Souern Hem.
def random_cities_lat():#n=15
    rd_ct_df = PD.DataFrame()

    #--- Northern Hem. random
    latitude_north_step = 5
    latitude_north_pick = 27
    for x in range(0,80,latitude_north_step):
        temp_df = citipy_df[(citipy_df['Latitude'] > x) & (citipy_df['Latitude'] < (x+latitude_north_step))]

        temp_lenght = len(temp_df)
        n = latitude_north_pick if latitude_north_pick <= temp_lenght else temp_lenght

        rd_ct_df = rd_ct_df.append(temp_df.sample(n=n))

    #--- Southern Hem. random
    latitude_south_step = -5
    latitude_south_pick = 20
    for x in range(0,-55,latitude_south_step):
        temp_df = citipy_df[(citipy_df['Latitude'] < x) & (citipy_df['Latitude'] > (x+latitude_south_step))]

        temp_lenght = len(temp_df)
        n = latitude_south_pick if latitude_south_pick <= temp_lenght else temp_lenght

        rd_ct_df = rd_ct_df.append(temp_df.sample(n=n))


    return rd_ct_df
# ---