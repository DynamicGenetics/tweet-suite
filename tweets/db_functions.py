import sqlite3
from sqlite3 import Error
import logging
from tweets.text_processing import process_text, vader

logger = logging.getLogger(__name__)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        logger.warning(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logger.warning(e)


def create_tweets_tables(db_name):
    """Create the tables we need for places and tweets in the SQLite3 database."""

    sql_create_places_table = """CREATE TABLE IF NOT EXISTS places (
                                    id text PRIMARY KEY,
                                    country text,
                                    country_code text,
                                    full_name text,
                                    geo_bbox text,
                                    name text,
                                    place_type text
                                );"""

    sql_create_tweets_table = """ CREATE TABLE IF NOT EXISTS tweets (
                                        id integer PRIMARY KEY,
                                        tweet_id integer UNIQUE,
                                        author_id text NOT NULL,
                                        created_at text NOT NULL,
                                        tweet_text text NOT NULL,
                                        simple_text text,
                                        vader_pos real,
                                        vader_neg real,
                                        vader_neu real,
                                        vader_comp real,
                                        lang text,
                                        place_id text,
                                        like_count integer,
                                        quote_count integer,
                                        reply_count integer,
                                        retweet_count integer,
                                        referenced_tweet text,
                                        referenced_type text,
                                        FOREIGN KEY (place_id) REFERENCES places (id)
                                    ); """

    # create a database connection
    conn = create_connection(db_name)

    # create tables
    if conn is not None:
        # create places table
        create_table(conn, sql_create_places_table)

        # create tweets table
        create_table(conn, sql_create_tweets_table)

        logger.info(
            "Tables tweets and places have been created in the database {}".format(
                db_name
            )
        )

    else:
        logger.warning("Error! cannot create the database connection.")


def create_place(conn, place):
    """
    Create a new place in the places table
    :param conn:
    :param place:
    :return: place id
    """
    sql = """ INSERT OR IGNORE INTO places(id,country,country_code,full_name,geo_bbox,name,place_type)
              VALUES(?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, place)
    conn.commit()
    return cur.lastrowid


def create_tweet(conn, tweet):
    """
    Create a new tweet
    :param conn:
    :param task:
    :return:
    """

    sql = """ INSERT OR IGNORE INTO tweets(tweet_id,author_id,created_at,tweet_text,simple_text,
            vader_pos,vader_neg,vader_neu,vader_comp,lang,place_id,like_count,quote_count,
            reply_count,retweet_count,referenced_tweet,referenced_type)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, tweet)
    conn.commit()
    return cur.lastrowid


def add_tweet_json(data, db_name):
    """Adds tweets to the database from the json object they are returned as.
    """
    # create a database connection
    conn = create_connection(db_name)

    with conn:

        # create new places
        for place in data["includes"]["places"]:
            new_place = (
                place["id"],
                place["country"],
                place["country_code"],
                place["full_name"],
                str(place["geo"]["bbox"]),
                place["name"],
                place["place_type"],
            )
            create_place(conn=conn, place=new_place)

        for tweet in data["data"]:
            vader_sentiment = vader(tweet["text"])
            try:
                new_tweet = (
                    tweet["id"],
                    tweet["author_id"],
                    tweet["created_at"],
                    tweet["text"],
                    process_text(tweet["text"]),
                    vader_sentiment["pos"],
                    vader_sentiment["neg"],
                    vader_sentiment["neu"],
                    vader_sentiment["compound"],
                    tweet["lang"],
                    tweet["geo"]["place_id"],
                    tweet["public_metrics"]["like_count"],
                    tweet["public_metrics"]["quote_count"],
                    tweet["public_metrics"]["reply_count"],
                    tweet["public_metrics"]["retweet_count"],
                    tweet["referenced_tweets"][0]["id"],
                    tweet["referenced_tweets"][0]["type"],
                )
            except KeyError:  # In the case that there is no referenced tweet
                new_tweet = (
                    tweet["id"],
                    tweet["author_id"],
                    tweet["created_at"],
                    tweet["text"],
                    process_text(tweet["text"]),
                    vader_sentiment["pos"],
                    vader_sentiment["neg"],
                    vader_sentiment["neu"],
                    vader_sentiment["compound"],
                    tweet["lang"],
                    tweet["geo"]["place_id"],
                    tweet["public_metrics"]["like_count"],
                    tweet["public_metrics"]["quote_count"],
                    tweet["public_metrics"]["reply_count"],
                    tweet["public_metrics"]["retweet_count"],
                    None,
                    None,
                )

            create_tweet(conn=conn, tweet=new_tweet)

    logger.info(
        "Processed {} tweets and {} places.".format(
            len(data["data"]), len(data["includes"]["places"])
        )
    )


def get_earliest_tweet(db_name):
    """
    Query to get the last tweet in the db.
    :param db_name: name of the db to connect to
    """

    # create a database connection
    conn = create_connection(db_name)
    cur = conn.cursor()

    # Run a query to get the time of the latest ID from the tweets in the database
    cur.execute(
        "SELECT created_at FROM tweets WHERE ID = (SELECT MAX(ID) FROM tweets);"
    )
    latest_tweet = cur.fetchone()

    # Return the time
    if latest_tweet is not None:
        return latest_tweet[0]
    else:
        return None
