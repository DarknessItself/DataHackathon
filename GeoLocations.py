#get geocoding data from address passed via command line
#has to do some funky stuff instead of just parsing webpage
#as an xml file because google puts api response data in
#a pre tag, which does not play nice with python... :(
#uses googles geocoding api
#ben jollymore 2019

import json
import urllib
import requests
import sys
import time
import argparse

types = ["accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station", "cafe", "campground", "car_dealer","car_rental","car_repair","car_wash","casino","cemetery","church","city_hall","clothing_store","convenience_store","courthouse","dentist","department_store","doctor","electrician","electronics_store","embassy","fire_station","florist","funeral_home","furniture_store","gas_station","gym","hair_care","hardware_store","hindu_temple","home_goods_store","hospital","insurance_agency","jewelry_store","laundry","lawyer","library","liquor_store","local_government_off", "locksmith", "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "museum", "night_club", "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office", "real_estate_agency", "restaurant", "roofing_contractor", "rv_park", "school", "shoe_store", "shopping_mall", "spa", "stadium", "storage", "store", "subway_station", "supermarket", "synagogue", "taxi_stand", "train_station", "transit_station", "travel_agency", "veterinary_care", "zoo" ]


isInteresting = False

parser = argparse.ArgumentParser(description="Parse the thing")
parser.add_argument('stringname', metavar='N', type=str, nargs='+', 
	help="Address for the building")
parser.add_argument('--fb', dest='printPost', help="Find the building type",
	action="store_true")

args=parser.parse_args()


#
url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
urlplaces = 'https://maps.googleapis.com/maps/api/place/details/json?'
key = '&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'
APIkey = 'AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'

#https://python.gotrained.com/google-places-api-extracting-location-data-reviews/
def search_places_by_coordinate(location, radius):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    places = [] 	#Premake the return array

    #Define the search parameters
    params = {
        'location': location,
        'radius': radius,
        'types': ",".join(types),
        'key': APIkey
    }

    res = requests.get(endpoint_url, params = params)
    results =  json.loads(res.content)
    places.extend(results['results'])
    time.sleep(2)
   
    while "next_page_token" in results:
        params['pagetoken'] = results['next_page_token'],
        res = requests.get(endpoint_url, params = params)
        results = json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
    
    return places

address = args.stringname[0]
print(address)
addressSendable = address.replace(" ", "+")

query = url + addressSendable + key
page = requests.get(query)
geoData = page.json()

try:
	place_id = geoData["results"][0]['place_id']
except KeyError:
	print("Failed")
	place_id = ""

print(place_id)

lattitude = geoData['results'][0]['geometry']['location']['lat']
longitude = geoData['results'][0]['geometry']['location']['lng']
addressInfo = []

if place_id != "" and args.printPost:
	places = search_places_by_coordinate(
		",".join([str(lattitude), str(longitude)]), "50")
	
	count = 0
	for x in places:				
		count += 1
		try:
			print("%2d: Name: %s, Address %s"%(count, x['name'], x['vicinity']))
		except KeyError:
			print("Name: %s, No address found"% x['name'])


print("\nBens Code\n")
for i in geoData['results'][0]['address_components']:
	#if (i['types'][0] != "route" and i['types'][0] != "street_number"):
	if i['long_name'] not in addressInfo:
		addressInfo.append(i['long_name'])

print("Lattitude: ", lattitude)
print("Longitude: ", longitude)
for i in addressInfo:
	print(i)


if isInteresting:
	print(
		"============================================"
		"            INTERESTING ADDRESS             "
		"============================================")