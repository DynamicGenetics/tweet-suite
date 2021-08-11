import os
import logging
import schedule

from tweets.db_functions import Database
from tweets.tweet_functions import FullArchiveSearch
from tweets.geolocation import MatchPlaces
from tweets import DB

# Set up logging
logging.basicConfig(
    filename="twitter.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Initialise logger
logger = logging.getLogger(__name__)

# Now set the twitter collection function to run every day
logger.info("Starting scheduler...")
# schedule.every().day.at("12:40").do(get_tweets(DB_NAME))

# Database(DB).get_unmatched_tweets()
def daily_job():
    # Set up the database object
    db = Database(DB)
    # Run the full archive search to update the tweets to midnight yesterday
    FullArchiveSearch(db).get_tweets()
    # Now, get the matched places, passing in the db of places currently unmatched
    matched = MatchPlaces(db.get_unmatched_places()).get()
    # Write these results to the database
    db.write_matched_places(matched)


if __name__ == "__main__":
    daily_job()
