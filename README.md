# cl_markets

This is a simple command-line utility for determining the nearest craigslist marketplace to a given location, such as "Sammamish, WA".

## Prerequisites

You'll need python 2.7.

There are three dependencies - requests, beautifulsoup and googlemaps - which can all be installed as follows:

```
pip install -U -r requirements.txt 
```

To use the googlemaps API you'll need to create a free account and copy your key into a file secrets.py, along with the name of your sqlite database file, as follows:

```
# module: secrets.py
# google maps API key
KEY = 'your_key_here'

# database file
DB_FILE = 'name_of_your_database_file'
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