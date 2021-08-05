import sqlite3
from sqlite3 import Error
import json


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
        print(e)

    return conn


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
    print("Place added")
    return cur.lastrowid


def create_tweet(conn, tweet):
    """
    Create a new tweet
    :param conn:
    :param task:
    :return:
    """

    sql = """ INSERT OR IGNORE INTO tweets(id,author_id,created_at,tweet_text,lang,place_id,like_count,quote_count,reply_count,retweet_count,referenced_tweet,referenced_type)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, tweet)
    conn.commit()
    print("Tweet added")
    return cur.lastrowid


def add_tweet_json(data):

    # create a database connection
    conn = create_connection(r"tweets.db")

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

            try:
                new_tweet = (
                    tweet["id"],
                    tweet["author_id"],
                    tweet["created_at"],
                    tweet["text"],
                    tweet["lang"],
                    tweet["geo"]["place_id"],
                    tweet["public_metrics"]["like_count"],
                    tweet["public_metrics"]["quote_count"],
                    tweet["public_metrics"]["reply_count"],
                    tweet["public_metrics"]["retweet_count"],
                    tweet["referenced_tweets"][0]["id"],
                    tweet["referenced_tweets"][0]["type"],
                )
            except KeyError: # In the case that there is no referenced tweet
                new_tweet = (
                    tweet["id"],
                    tweet["author_id"],
                    tweet["created_at"],
                    tweet["text"],
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


if __name__ == "__main__":

    with open("./data.json") as f:
        data = json.load(f)
    
    add_tweet_json(data)
