# utils/data_fetcher.py

import requests
import os
from bs4 import BeautifulSoup

def get_organic_locations(latitude, longitude, radius=5000):
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    endpoint_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'keyword': 'organic',
        'type': 'restaurant|grocery_or_supermarket|food',
        'key': api_key
    }

    res = requests.get(endpoint_url, params=params)
    results = res.json().get('results', [])

    organic_locations = []
    for place in results:
        location = {
            'name': place.get('name'),
            'place_id': place.get('place_id'),
            'address': place.get('vicinity'),
            'rating': place.get('rating'),
            'user_ratings_total': place.get('user_ratings_total'),
            'latitude': place['geometry']['location']['lat'],
            'longitude': place['geometry']['location']['lng'],
            'website': get_place_website(place.get('place_id'))
        }
        organic_locations.append(location)

    return organic_locations

def get_place_website(place_id):
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    endpoint_url = 'https://maps.googleapis.com/maps/api/place/details/json'

    params = {
        'place_id': place_id,
        'fields': 'website',
        'key': api_key
    }

    res = requests.get(endpoint_url, params=params)
    result = res.json().get('result', {})
    website = result.get('website')
    return website

def fetch_business_info(website_url):
    headers = {'User-Agent': 'Your User Agent'}
    try:
        response = requests.get(website_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching business info: {e}")
    return None
