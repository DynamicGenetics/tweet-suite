"""
Code from https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Full-Archive-Search/full-archive-search.py
"""

import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("SEARCHTWEETS_BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/all"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {
    "query": "place_country:GB place:Wales",
    "start_time": "2020-03-01T00:00:00Z",
    "end_time": "2020-03-02T00:00:00Z", 
    "tweet.fields": "id,created_at,author_id,text,public_metrics,geo,lang,referenced_tweets",
    "place.fields": "country,country_code,full_name,geo,id,name,place_type",
    'expansions': "geo.place_id"
}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
