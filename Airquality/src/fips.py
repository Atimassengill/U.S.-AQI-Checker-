import requests
import urllib
from geopy.geocoders import Nominatim
import geocoder


def change_place_to_cordinates(place):
    #Uses geocoder which takes in a city name and returns a lat and long value of the location 
    #Then takes that lat and long value and makes an api requests to get the fips code of the area
    global lat_long_txt, lat, lon, location


    geolocator = Nominatim(user_agent="Your_Name")
    location = geolocator.geocode(place)
    lat_long_txt = '&lat={lat}&lon={long}'.format(lat=location.latitude,long=location.longitude)  

    lat = location.latitude
    lon = location.longitude
    params = urllib.parse.urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
    url = 'https://geo.fcc.gov/api/census/block/find?' + params
    response = requests.get(url)
    data = response.json()

    return data['County']['FIPS']


