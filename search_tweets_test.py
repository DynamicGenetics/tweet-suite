"""
Attempting to do a full archive search using the search_tweets v2 module by TwitterDev. 
Module documentation here: https://github.com/twitterdev/search-tweets-python/tree/v2
"""

import os
from searchtweets import (
    ResultStream,
    gen_request_parameters,
    load_credentials,
    collect_results,
)

# search_args = load_credentials()

query = gen_request_parameters(
    query="place_country:GB place:Wales",
    granularity=None,
    results_per_call=None,
    start_time="2020-03-01",
    end_time="2020-03-02",
    tweet_fields="id,created_at,author_id,text,public_metrics,geo,lang,referenced_tweets",
    place_fields="country,country_code,full_name,geo,id,name,place_type",
    expansions="geo.place_id",
)

print(query)


# tweets = collect_results(query,
#                          max_tweets=100,
#                          result_stream_args=search_args) # change this if you need to


rs = ResultStream(
    bearer_token=os.environ.get("SEARCHTWEETS_BEARER_TOKEN"),
    endpoint=os.environ.get("SEARCHTWEETS_ENDPOINT"),
    request_parameters=query,
    max_results=500,
    max_pages=1,
)

tweets = list(rs.stream())


with open("data.json", "w", encoding="utf-8") as f:
    json.dump(tweets, f, ensure_ascii=False, indent=4)

