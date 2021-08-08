import os
import logging
import schedule

from tweets.db_functions import create_tweets_tables
from tweets.tweet_functions import get_tweets

DB_NAME = "phw_tweets.db"

# Set up logging
logging.basicConfig(
    filename="twitter.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Initialise logger
logger = logging.getLogger(__name__)

# If the database file doesn't exist then create it
if not os.path.exists(DB_NAME):
    create_tweets_tables(DB_NAME)
    logger.info("Database created, named {}".format(DB_NAME))
else:
    logger.info("Using existing database named {}".format(DB_NAME))

# Now set the twitter collection function to run every day
logger.info("Starting scheduler...")
# schedule.every().day.at("12:40").do(get_tweets(DB_NAME))

get_tweets(DB_NAME)
