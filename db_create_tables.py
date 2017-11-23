#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module: db_create_tables.py
"""
The database schema for cl_markets
"""
import sqlite3
from secrets import DB_FILE
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Create table cl_states
c.execute('''CREATE TABLE IF NOT EXISTS cl_states (
    state_id INTEGER PRIMARY KEY,
    state TEXT, 
    url TEXT,
    CONSTRAINT state_unique UNIQUE (state)
)''')

# Create table cl_markets
c.execute('''CREATE TABLE IF NOT EXISTS cl_markets (
    market_id INTEGER PRIMARY KEY,
    location_name TEXT,
    domain TEXT,
    state TEXT, 
    latitude REAL,
    longitude REAL,
    FOREIGN KEY(state) REFERENCES cl_states(state),
    CONSTRAINT name_unique UNIQUE (location_name)
)''')

# Create table locations - a cache of previously-geocoded locations
# so they need not be looked up again in google maps API
c.execute('''CREATE TABLE IF NOT EXISTS locations ( 
    location_id INTEGER PRIMARY KEY, 
    location_name TEXT, 
    latitude REAL, 
    longitude REAL, 
    CONSTRAINT name_unique UNIQUE (location_name))
''')

conn.commit()   # Save (commit) the changes
conn.close()   # Close the connection after all changes committed