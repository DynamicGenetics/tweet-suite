import os
import logging
import schedule

from tweets.db_functions import Database
from tweets.tweet_functions import FullArchiveSearch

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

FullArchiveSearch(Database("phw_tweets.db")).get_tweets()

