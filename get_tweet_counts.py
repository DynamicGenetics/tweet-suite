"""This is based on sample code from
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Full-Archive-Tweet-Counts/full_archive_tweet_counts.py
"""

import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("SEARCHTWEETS_BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/counts/all"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main(query_params):
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":

    main(  # Optional params: start_time,end_time,since_id,until_id,next_token,granularity
        query_params={
            "query": "place_country:GB place:Wales",
            "granularity": "day",
            "start_time": "2020-03-01T00:00:00Z",
            "end_time": "2020-04-01T00:00:00Z",
        }
    )

    main(  # Optional params: start_time,end_time,since_id,until_id,next_token,granularity
        query_params={
            "query": "place_country:GB place:Wales",
            "granularity": "day",
            "start_time": "2020-04-01T00:00:00Z",
            "end_time": "2020-05-01T00:00:00Z",
        }
    )

    main(  # Optional params: start_time,end_time,since_id,until_id,next_token,granularity
        query_params={
            "query": "place_country:GB place:Wales",
            "granularity": "day",
            "start_time": "2020-05-01T00:00:00Z",
            "end_time": "2020-06-01T00:00:00Z",
        }
    )

    main(  # Optional params: start_time,end_time,since_id,until_id,next_token,granularity
        query_params={
            "query": "place_country:GB place:Wales",
            "granularity": "day",
            "start_time": "2020-06-01T00:00:00Z",
            "end_time": "2020-07-01T00:00:00Z",
        }
    )

    main(  # Optional params: start_time,end_time,since_id,until_id,next_token,granularity
        query_params={
            "query": "place_country:GB place:Wales",
            "granularity": "day",
            "start_time": "2020-07-01T00:00:00Z",
            "end_time": "2020-08-01T00:00:00Z",
        }
    )

    main(  # Optional params: start_time,end_time,since_id,until_id,next_token,granularity
        query_params={
            "query": "place_country:GB place:Wales",
            "granularity": "day",
            "start_time": "2020-08-01T00:00:00Z",
            "end_time": "2020-09-01T00:00:00Z",
        }
    )

