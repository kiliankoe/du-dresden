import tweepy
import configparser
import sqlite3 as db
import saxophone
import html
import re
from time import sleep
from datetime import *


def cut_140_chars(tweet):
    """Cuts a string down to 140 characters."""
    if tweet is None:
        return ''
    elif len(tweet) > 140:
        return ''.join(list(tweet)[:139]) + '…'
    else:
        return tweet


def is_retweet(tweet):
    """Returns the beginning of a retweet 'RT @account: ' if a tweet is a retweet, else None."""
    match = re.match('RT @.*?:', tweet)
    if match is None:
        return None
    return match.group(0)


def is_mention(tweet):
    """Returns if a tweet is only a mention"""
    match = re.search('\A@.*', tweet)
    if match is None:
        return False
    return True


def get_twitter_api():
    """Returns a reference to the Twitter API with the saved credentials."""
    secrets = configparser.ConfigParser()
    secrets.read('secrets.ini')

    auth = tweepy.OAuthHandler(secrets['Twitter']['consumer_key'], secrets['Twitter']['consumer_secret'])
    auth.set_access_token(secrets['Twitter']['access_token'], secrets['Twitter']['access_token_secret'])

    tw_api = tweepy.API(auth)
    return tw_api


def get_last_tweets(api, count):
    """Returns a custom amount of recent tweets for the account @tudresden_de."""
    return api.user_timeline(id='tudresden_de', count=count)


def process_tweet(tweet):
    """Prepare a tweet message for sending"""
    if is_mention(tweet):
        return
    if is_retweet(tweet):
        new_tweet = is_retweet(tweet) + ' ' + saxophone.translate(re.sub('RT @.*?:', '', html.unescape(tweet)),
                                                                  engine='twitter')
    else:
        new_tweet = saxophone.translate(html.unescape(tweet), engine='twitter')
    return cut_140_chars(new_tweet)


def send_tweet(api, tweet):
    """Sends a tweet on the account @dudresden."""
    if tweet is None:
        return
    sleep(2)
    api.update_status(tweet)


def db_get_all():
    """Get all IDs in the database."""
    con = db.connect('data.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT id FROM "Twitter"')
        results = [row[0] for row in cur]
        cur.close()
    con.close()
    return results


def db_insert_id(tweet_id, tweet_status):
    """Insert an ID into the database."""
    con = db.connect('data.db')
    with con:
        cur = con.cursor()
        cur.execute('INSERT into "Twitter" VALUES (?, ?);', (str(tweet_id), tweet_status,))
        cur.close()
    con.close()


def do_stuff():
    api = get_twitter_api()
    for status in reversed(get_last_tweets(api, 20)):
        try:
            db_insert_id(status.id, status.text)
            send_tweet(api, process_tweet(status.text))
        except db.IntegrityError:
            # Validate a tweet's existence on the database, works great :P
            continue

if __name__ == '__main__':
    do_stuff()

# TODO: Sort these functions in a sensible way
