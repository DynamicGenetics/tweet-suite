# Tweet Suite

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DOI](https://zenodo.org/badge/393027802.svg)](https://zenodo.org/badge/latestdoi/393027802)

This package, when run, will execute a query every day that collects all tweets from Wales for the past 7 days (if running for the first time), or since the last tweet collected.
It uses Twitter's V2 API. 

When run it will set up an SQLite3 database in the location specified to the main script which saves tweets, their basic information and their sentiment scores from the [VADER sentiment algorithm](https://github.com/cjhutto/vaderSentiment) in a table called `tweets`.  
A table called `places` then saves the geo expansion information requested in the query.  
Finally, a table called `matchedplaces` saves the result of each place matched to a Welsh local authority using an algorithm defined in the `tweets/geo.py` file. 

## Authors  

This package was written by [ninadicara](https://github.com/ninadicara), [altanner](https://github.com/altanner), and [leriomaggio](https://github.com/leriomaggio). 

## Good to know  

### API Tokens  
This uses the academic API, so you need an approved account with a bearer token.  
If you'd like this to work out the box then you'll need to set 
the bearer token as an environment variable called `SEARCHTWEETS_BEARER_TOKEN`. 

### Query  
Currently the query returns tweets with basic information and requests the geo expansion.  
If you change the query you'll also need to edit the SQL tables and data entry functions. 
These are in `tweets/database.py`, called `create_tweets_tables()` and `add_tweet_json()`. 

### Database  
The database is SQLite3, for ease and as an alternative to CSV.
The schema for the database can be seen in the setup functions as part of the `Database` class in `tweets/database.py`. 
There is a foreign key between `place_id` in the `tweets` and `matchedplaces` tables that link to the primary `id` entry in the `places` table. 

## Data statement  

Source: Office for National Statistics licensed under the [Open Government Licence v.3.0](http://www.nationalarchives.gov.uk/doc/open-government-licence).  
Contains OS data © Crown copyright and database right 2019.  
This package uses [boundary data of Welsh Local Authorities](https://geoportal.statistics.gov.uk/datasets/local-authority-districts-december-2019-boundaries-uk-buc) (see `utils/la_keys.geojson`). 
