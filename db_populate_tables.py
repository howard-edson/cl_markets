#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module: db_populate_tables.py
"""
Populate the database for cl_markets
"""
import sqlite3
from secrets import DB_FILE, KEY
import cl_markets as cl
gmaps = cl.googlemaps.Client(key=KEY)
conn = sqlite3.connect(DB_FILE)

#############################################################
# Populate cl_states
#############################################################
# these are a list of the state-level craigslist pages, which
# contain links to the actual markets/cities in state.
# In a few cases there are no sub-pages and the state page is 
# the market.
c = conn.cursor()

states = [
    ('AL', 'https://geo.craigslist.org/iso/us/al'),
    ('AK', 'https://geo.craigslist.org/iso/us/ak'),
    ('AZ', 'https://geo.craigslist.org/iso/us/az'),
    ('AR', 'https://geo.craigslist.org/iso/us/ar'),
    ('CA', 'https://geo.craigslist.org/iso/us/ca'),
    ('CO', 'https://geo.craigslist.org/iso/us/co'),
    ('CT', 'https://geo.craigslist.org/iso/us/ct'),
    ('DC', 'https://geo.craigslist.org/iso/us/dc'),
    ('DE', 'https://geo.craigslist.org/iso/us/de'),
    ('FL', 'https://geo.craigslist.org/iso/us/fl'),
    ('GA', 'https://geo.craigslist.org/iso/us/ga'),
    ('HI', 'https://geo.craigslist.org/iso/us/hi'),
    ('ID', 'https://geo.craigslist.org/iso/us/id'),
    ('IL', 'https://geo.craigslist.org/iso/us/il'),
    ('IN', 'https://geo.craigslist.org/iso/us/in'),
    ('IA', 'https://geo.craigslist.org/iso/us/ia'),
    ('KS', 'https://geo.craigslist.org/iso/us/ks'),
    ('KY', 'https://geo.craigslist.org/iso/us/ky'),
    ('LA', 'https://geo.craigslist.org/iso/us/la'),
    ('ME', 'https://geo.craigslist.org/iso/us/me'),
    ('MD', 'https://geo.craigslist.org/iso/us/md'),
    ('MA', 'https://geo.craigslist.org/iso/us/ma'),
    ('MI', 'https://geo.craigslist.org/iso/us/mi'),
    ('MN', 'https://geo.craigslist.org/iso/us/mn'),
    ('MS', 'https://geo.craigslist.org/iso/us/ms'),
    ('MO', 'https://geo.craigslist.org/iso/us/mo'),
    ('MT', 'https://geo.craigslist.org/iso/us/mt'),
    ('NC', 'https://geo.craigslist.org/iso/us/nc'),
    ('NE', 'https://geo.craigslist.org/iso/us/ne'),
    ('NV', 'https://geo.craigslist.org/iso/us/nv'),
    ('NJ', 'https://geo.craigslist.org/iso/us/nj'),
    ('NM', 'https://geo.craigslist.org/iso/us/nm'),
    ('NY', 'https://geo.craigslist.org/iso/us/ny'),
    ('NH', 'https://geo.craigslist.org/iso/us/nh'),
    ('ND', 'https://geo.craigslist.org/iso/us/nd'),
    ('OH', 'https://geo.craigslist.org/iso/us/oh'),
    ('OK', 'https://geo.craigslist.org/iso/us/ok'),
    ('OR', 'https://geo.craigslist.org/iso/us/or'),
    ('PA', 'https://geo.craigslist.org/iso/us/pa'),
    ('RI', 'https://geo.craigslist.org/iso/us/ri'),
    ('SC', 'https://geo.craigslist.org/iso/us/sc'),
    ('SD', 'https://geo.craigslist.org/iso/us/sd'),
    ('TN', 'https://geo.craigslist.org/iso/us/tn'),
    ('TX', 'https://geo.craigslist.org/iso/us/tx'),
    ('UT', 'https://geo.craigslist.org/iso/us/ut'),
    ('VT', 'https://geo.craigslist.org/iso/us/vt'),
    ('VA', 'https://geo.craigslist.org/iso/us/va'),
    ('WA', 'https://geo.craigslist.org/iso/us/wa'),
    ('WV', 'https://geo.craigslist.org/iso/us/wv'),
    ('WI', 'https://geo.craigslist.org/iso/us/wi'),
    ('WY', 'https://geo.craigslist.org/iso/us/wy')
]
c.executemany('INSERT INTO cl_states (state, url) VALUES (?,?)', states)
print "Populated cl_states with {} records".format(len(states))
conn.commit()   # Save (commit) the changes


#############################################################
# Populate cl_markets (not geocoded yet)
#############################################################
c = conn.cursor()

# States with one page for the whole state (no submarkets)
nosub_states = ['WY', 'DC', 'DE', 'HI', 'RI', 'ME', 'NH', 'VT']

# for each state, url in cl_states, scrape craigslist for the markets
# in that state; blacklist states are special cases.
us_markets = [] #('bellingham, wa', 'bellingham.craigslist.org', 'WA')
for row in c.execute('SELECT state, url FROM cl_states'):
    state, url = row  # unpack the row tuple
    if state not in nosub_states:
        soup = cl.get_page(url)
        # a list of (loc, link, state) tuples
        state_markets = cl.get_cities(soup, state)
        us_markets += state_markets
conn.commit()

# Now add the special case states with no sub-markets
nosub_markets = [
    ('Wyoming', 'wyoming.craigslist.org', 'WY'),
    ('washington DC', 'washingtondc.craigslist.org', 'DC'),
    ('Delaware', 'delaware.craigslist.org', 'DE'),
    ('Hawaii', 'honolulu.craigslist.org', 'HI'),
    ('Rhode Island', 'providence.craigslist.org', 'RI'),
    ('Maine', 'maine.craigslist.org', 'ME'),
    ('New Hampshire', 'nh.craigslist.org', 'NH'),
    ('Vermont', 'vermont.craigslist.org', 'VT'),
]
us_markets += nosub_markets

# Now insert all the us_markets at once, not geocoded yet!
c.executemany('''INSERT INTO cl_markets (
        location_name,
        domain,
        state
    ) VALUES (?,?,?)''', us_markets)

print "Populated cl_markets with {} records.".format(len(us_markets))
conn.commit()

#############################################################
# Geocode cl_markets 
#############################################################
c_read = conn.cursor()
c_write = conn.cursor()

for row in c_read.execute('SELECT market_id, location_name FROM cl_markets'):
    market_id, location = row  # unpack the row tuple
    # now get lat/lng for this location
    geo = cl.geocode(location, gmaps)
    lat = geo['lat']
    lng = geo['lng']
    # add the state's marketplaces to the marketplace dictionary

    c_write.execute('''UPDATE cl_markets
                SET latitude=?, longitude=?
                WHERE market_id=?''', (lat, lng, market_id)
    )
    conn.commit()
print "Geocoded cl_markets"

#############################################################
# Populate locations 
#############################################################
# Initialize the locations table with the geocoded locations we already have
# in cl_markets.
c = conn.cursor()

c.execute('''INSERT INTO locations (location_name, latitude, longitude)
    SELECT location_name, latitude, longitude FROM cl_markets
''')
print "Initialized locations table with geocoded locations from cl_markets"

conn.commit()   # Save (commit) the changes
conn.close()   # Close the connection after all changes committed