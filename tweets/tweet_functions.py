import requests
import os
from retry import retry
import logging

logger = logging.getLogger(__name__)

from tweets.db_functions import add_tweet_json

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
    print(response.status_code)
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
