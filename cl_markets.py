#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module: cl_markets.py
"""
Utility functions for the cl_markets app
"""
from bs4 import BeautifulSoup
import bs4
import requests
import re
import googlemaps
from secrets import KEY # google maps API key
from math import radians, cos, sin, asin, sqrt

gmaps = googlemaps.Client(key=KEY)     # googlemaps API key
p = re.compile('\w+.craigslist.org')   # regex pattern for finding url in a craigslist page


def get_page(url):
    "return a web page as a beautiful soup object"
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def get_cities(soup, state):
    """
    return a list of cities and CL marketplace URLs from a soup object 
    containing a list of CL cities in the given state.
    """
    output = [] 
    ul = soup.find("ul", class_="geo-site-list")
    # iterate through the html list items
    for li in ul.find_all("li"):
        a = li.find("a")
        link = a.get('href')
        link = unicode(link) # convert soup object to text
        m = p.search(link)   # just keep the '*.craigslist.org' part, if possible
        if m:
            link = m.group()
        city = a.contents[0] # this is the name of the city corresponding to the link
        # if craigslist bolds a city name then it needs additional processing
        if not (isinstance(city, bs4.element.NavigableString)):
            city = city.get_text()
        city = unicode(city) # convert soup object to text
        city = city.split('/')[0] # keep only the first city name if several
        city = city.split('-')[0].strip().title() # strip white space, title case
        location = '{city}, {state}'.format(city=city.lower(), state=state.lower())
        output.append((location, link, state))
    return output


def geocode(address, gmaps):
    "Return lat/lng for an address"
    geocode_result = gmaps.geocode(address)
    lat_lng = geocode_result[0]['geometry']['location']
    return lat_lng


def miles(lng1, lat1, lng2, lat2):
    "Return the distance in miles between two lat/lng pairs"
    # convert decimal degrees to radians 
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    # haversine formula 
    dlng = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in miles. Use 6371 for kilometers.
    return c * r
