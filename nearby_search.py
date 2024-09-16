import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.geocoders import Photon
import csv
import pandas as pd
from phone_number import populate_phone_numbers



def nearby_search(postcode, radius, API_KEY, COUNTRY):
    try:
        lat, long = get_lat_long(postcode)
    except:
        lat, long = '51.467590', '-3.195243'
    pharmacies = search_pharmacies(lat, long, radius, API_KEY)    
    if 'results' in pharmacies:
        try:
            origin = (lat, long)
            pharmacy_list = filter_pharmacies(pharmacies, origin)      
                        
            # convert dict to dataframe then sort by distance 
            df = pd.DataFrame(pharmacy_list)
            pharmacy_list = df.sort_values('Distance (m)')
            pharmacies = populate_phone_numbers(COUNTRY, pharmacy_list)
            # flag possible duplicates
            # gather known and unknown into 2 seperate dataframes
            unknown_number = pharmacies.loc[pharmacies['Number'] == "Unknown"]
            known_number = pharmacies.loc[pharmacies['Number'] != "Unknown"]
            
            # drop duplicates from known number pharmacies
            filtered_df = known_number.sort_values(['Pharmacy', 'Number'], ascending=[True, False]).drop_duplicates('Pharmacy').sort_index()
            # build group of dataframes
            frames = [unknown_number, filtered_df]
            # join filtered dataframe and unknown numbers and sort by distance
            pharmacies = pd.concat(frames).sort_values('Distance (m)')
            return(pharmacies)
        except:
            empty_df = pd.DataFrame()
            return(empty_df)
    else:
        print("No pharmacies found.")
    

# Function to get the latitude and longitude of a postcode
def get_lat_long(postcode):
    geolocator = Nominatim(user_agent="pharmacy_locator")
    location = geolocator.geocode(postcode)
    return (location.latitude, location.longitude)

# Function to search for pharmacies within the specified radius
def search_pharmacies(lat, long, radius, API_KEY):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius={radius}&type=pharmacy&keyword=pharmacy&key={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_postcode(lat, lon):
    # Initialize the geolocator with Nominatim
    geolocator = Nominatim(user_agent="geoapiExercises")  
    # Reverse geocode the coordinates to get an address
    location = geolocator.reverse((lat, lon), exactly_one=True)
    # Extract the postcode from the address
    if location and 'postcode' in location.raw['address']:
        return location.raw['address']['postcode']
    else:
        return "Postcode not found"    


# Function to filter and display pharmacies
def filter_pharmacies(pharmacies, origin):
    results = []
    for pharmacy in pharmacies['results']:
        pharmacy_name = pharmacy['name']
        pharmacy_address = pharmacy.get('vicinity', 'Address not available')
        pharmacy_location = (pharmacy['geometry']['location']['lat'], pharmacy['geometry']['location']['lng'])
        distance = round(geodesic(origin, pharmacy_location).meters, 0)
        
        # create dictionary from pharmacy data and copy row to results list
        pharmacy_data  = {"Pharmacy": pharmacy_name, "Address": pharmacy_address, "Distance (m)": distance}
        results.append(pharmacy_data.copy())
    return results

