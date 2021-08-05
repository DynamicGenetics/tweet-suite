import sqlite3
from sqlite3 import Error


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
        print(e)


def create_tweets_tables():
    database = r"tweets.db"

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
                                        author_id text NOT NULL,
                                        created_at text NOT NULL,
                                        tweet_text text NOT NULL,
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
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_places_table)

        # create tasks table
        create_table(conn, sql_create_tweets_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    create_tweets_tables()
