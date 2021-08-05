import os
import logging

from tweets.tweet_functions import fetch_twitter_data

from tweets.db_functions import create_tweets_tables, get_earliest_tweet

from tweets import DB_NAME, QUERY_START, QUERY_END

# Set up logging
logging.basicConfig(
    filename="twitter.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Initialise logger
logger = logging.getLogger("scheduler")

# If the database file doesn't exist then create it
if not os.path.exists(DB_NAME):
    create_tweets_tables(DB_NAME)

# In case the Twitter connection goes down we want to be able to restart from where we left off.
# This means changing the query so we are searching from the last given point.
# Importantly the results are given from the end date backwards, so we need to change the end date not the start

earliest_tweet = get_earliest_tweet(DB_NAME)

if earliest_tweet is None:
    END_TIME = QUERY_END
else:
    END_TIME = earliest_tweet

logger.info("Query established with an end time of {}".format(END_TIME))


# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
# NB if changing the query you'll probably need to change the database fields etc so do with caution!
QUERY = {
    "query": "place_country:GB place:Wales",
    "start_time": QUERY_START,
    "end_time": END_TIME,
    "tweet.fields": "id,created_at,author_id,text,public_metrics,geo,lang,referenced_tweets",
    "place.fields": "country,country_code,full_name,geo,id,name,place_type",
    "expansions": "geo.place_id",
    "max_results": 500,
}

# Run the api calls to collect the data
fetch_twitter_data(QUERY, DB_NAME)
