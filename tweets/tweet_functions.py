import requests
import os
from retry import retry
import logging

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

from tweets.db_functions import add_tweet_json, get_latest_tweet

# Set the bearer token and the search URL
bearer_token = os.environ.get("SEARCHTWEETS_BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/all"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


@retry(Exception, tries=3, delay=3, backoff=5)
def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    if response.status_code == 429:
        raise Exception("Rate limited")
    if response.status_code != 200:
        raise Exception("Didn't get a 200 response...")
    return response.json()


def fetch_twitter_data(query_params, db_name):
    # Get the json response from Twitter
    json_response = connect_to_endpoint(search_url, query_params)
    # Add the data to the database
    add_tweet_json(json_response, db_name)

    # Whilst there is a next token option in the response, paginate through.
    while "next_token" in json_response["meta"]:
        query_params["next_token"] = json_response["meta"]["next_token"]
        json_response = connect_to_endpoint(search_url, query_params)
        add_tweet_json(json_response, db_name)


def start_time(db_name):
    """Get the time that the query needs to start from."""

    # Get the time of the most recent tweet in the dataframe
    latest_tweet = get_latest_tweet(db_name)

    # If there is no latest tweet then we need 7 days of data.
    if latest_tweet is None:
        # Set start time as midnight yesterday minus one week
        start_time = (yesterday() - timedelta(weeks=1)).strftime("%Y-%m-%dT") + (
            "23:59:00Z"
        )
        logger.info(
            "First run of scheduler - will collect 7 days of tweets since {}".format(
                start_time
            )
        )
    else:  # Otherwise, set the start time as the most recent date in the database
        start_time = latest_tweet
        logger.info("Updated start time is set as {}".format(start_time))

    return start_time


def yesterday():
    """Get the datetime for yesterday"""

    return datetime.now().date() - timedelta(days=1)


def get_tweets(db_name):

    start = start_time(db_name)
    # The end time must be at least 10 seconds before the request time, so take 30 seconds.
    end = yesterday().strftime("%Y-%m-%dT") + ("23:59:00Z")

    # Get the tweets between the start time we've set and now.
    query = {
        "query": "place_country:GB place:Wales",
        "start_time": start,
        "end_time": end,
        "tweet.fields": "id,created_at,author_id,text,public_metrics,geo,lang,referenced_tweets",
        "place.fields": "country,country_code,full_name,geo,id,name,place_type",
        "expansions": "geo.place_id",
        "max_results": 500,
    }

    # Now, pass this query to the function that actually fetches the data.
    fetch_twitter_data(query, db_name)

    logger.info("Tweets successfully collected.")

