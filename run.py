#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module: run.py
import sys
from secrets import DB_FILE, KEY
import sqlite3
import cl_markets as cl

gmaps = cl.googlemaps.Client(key=KEY)

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

location = sys.argv[1] if len(sys.argv) > 1 else 'seattle, wa'

# See if the location already exists in the locations table
location_lower = location.lower()
c.execute('''SELECT latitude, longitude 
            FROM locations 
            WHERE lower(location_name)=?''', (location_lower,))
result = c.fetchone()
conn.commit()

if result: # location already exists in the database
    lat1, lng1 = result
else:      # geocode the new location 
    geo = cl.geocode(location, gmaps)
    lat1 = geo['lat']
    lng1 = geo['lng']
    # write it to the locations table for future reference
    c.execute('''INSERT INTO locations (location_name, latitude, longitude)
                VALUES (?,?,?)''', (location_lower, lat1, lng1))
    conn.commit()

# now we have the location's geo, let's find the nearest craigslist market
# build a list of craigslist markets and the distance to each
distances = {}  # cl markets (domains) with distance from location
for row in c.execute('SELECT domain, latitude, longitude FROM cl_markets'):
    domain, lat2, lng2 = row  # unpack the row tuple
    # get the distance to location in question
    miles = int(cl.miles(lng1, lat1, lng2, lat2))
    distances[domain] = miles
conn.commit()

# Find the nearest craigslist market city and domain
nearest_city = min(distances, key=distances.get)
print "{} is {} miles from {}".format(nearest_city, distances[nearest_city], location)

conn.close()  # Done with the database