# cl_markets

This is a simple command-line utility for determining the nearest craigslist marketplace to a given location, such as "Sammamish, WA".

## Prerequisites

You'll need python 2.7.

There are three dependencies - requests, beautifulsoup and googlemaps - which can all be installed as follows:

```
pip install -U -r requirements.txt 
```

To use the [googlemaps API](https://developers.google.com/maps/documentation/geocoding/start) you'll need to create a free account and copy your key into a file secrets.py, along with the name of your sqlite database file, as follows:

```
######################
# module: secrets.py
######################

KEY = 'your_key_here'   # google maps API key
DB_FILE = 'db_filename' # database file 
```

## Instructions

Running db_create_tables.py will create your database file and schema.

Running db_populate_tables.py will populate the tables. This will take
several minutes, becuause it:
* scrapes craigslist state pages to get a list of markets in each state
* uses the google maps API to get lat/lng for each of some 450 markets.

When that is complete you can run the program from the command line, passing a location in quotes, as follows:

```
$ python run.py "anacortes, wa"
bellingham.craigslist.org is 17 miles from anacortes, wa
$
```

Locations are saved in a locations table so the distance can be calculated in the future without querying the google maps API again.

The google maps api can be used to calculate distance, but because the number of service calls per day is limited with a free account, the program calculates distances between two lat/lng pairs locally, using the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula).