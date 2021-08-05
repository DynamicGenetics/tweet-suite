# Tweet Suite

## Good to know

### API Tokens
This uses the academic API, so you need an approved account with a bearer token.  
If you'd like this to work out the box then you'll need to set 
the bearer token as an environment variable called `SEARCHTWEETS_BEARER_TOKEN`. 

### Query
Currently the query returns tweets with basic information and requests the geo expansion.  
If you change the query you'll also need to edit the SQL tables and data entry functions. 
These are in `tweets/db_functions.py`, called `create_tweets_tables()` and `add_tweet_json()`. 

You can change the start and end date of the query in `tweets/settings.py`

### Database
The database is SQLite3, for ease and as an alternative to CSV. The geo information from the tweets
and the tweet data itself is in two different tables called `tweets` and `places`. 
There is a foreign key between the place id in the `tweets` table and the id in the `places` table. 

