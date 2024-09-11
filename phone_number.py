import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def populate_phone_numbers(COUNTRY, data):       
    output = pd.DataFrame()
    phone_numbers = []

    # iterate through the pharmacies using the name and address to find the phone number for each
    for index, row in data.iterrows():
        business_name = row['Pharmacy']
        address = row['Address']
        phone_number = get_phone_number(business_name, address, COUNTRY)
        if phone_number:
            phone_numbers.append(phone_number)
        else:
            phone_numbers.append("Unknown")

    output = data.assign(Number=phone_numbers)
    return output
        

def get_phone_number(business_name, address, COUNTRY):
    # Format the search query
    query = f"{business_name} {address} {COUNTRY} phone number"
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"    
    # Set up headers to mimic a browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    print(url)
    # Send the request
    response = requests.get(url, headers=headers)
    
    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to retrieve information. Status code: {response.status_code}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # various phone number formats (I'm bad at regex)
    # this finds uk numbers so don't need the list anymore, but hey ho it took all morning.
    if COUNTRY == 'UK':    
        phone_number_patterns = [re.compile(r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$')]
    elif COUNTRY == 'NL':
        phone_number_patterns = [re.compile(r'^(?:0|(?:\+|00) ?31 ?)(?:(?:[1-9] ?(?:[0-9] ?){8})|(?:6 ?-? ?[1-9] ?(?:[0-9] ?){7})|(?:[1,2,3,4,5,7,8,9]\d ?-? ?[1-9] ?(?:[0-9] ?){6})|(?:[1,2,3,4,5,7,8,9]\d{2} ?-? ?[1-9] ?(?:[0-9] ?){5}))$')]
    
    # Search for phone number patterns in the text
    phone_numbers = []
    i = 0
    # loop through formats
    while i < len(phone_number_patterns):
        phone_pattern = phone_number_patterns[i]
        # loop through page finding phone numbers that match the regex pattern
        for element in soup.find_all(text=True):
            potential_numbers = re.findall(phone_pattern, element)
            phone_numbers.extend(potential_numbers)   
        i += 1    
        
    # Return the first phone number found, or None if no number is found
    return phone_numbers[0] if phone_numbers else None
   

def most_common(lst):
    return max(set(lst), key=lst.count)