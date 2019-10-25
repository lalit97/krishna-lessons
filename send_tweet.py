import tweepy
import textwrap
import get_tweet as gt
from config import conf


LIMIT = 280
CONSUMER_KEY = conf['twitter_api']['CONSUMER_KEY']
CONSUMER_SECRET = conf['twitter_api']['CONSUMER_SECRET']
ACCESS_KEY = conf['twitter_api']['ACCESS_KEY']
ACCESS_SECRET = conf['twitter_api']['ACCESS_SECRET']


def authenticate():
    ''' Handle tweepy auntentication'''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api


def format_tweets(tweets, string):
    ''' Format tweets such that each contains less than 280 character'''
    parts = textwrap.wrap(string, LIMIT)
    for part in parts:
        tweets.append(part)
    return tweets


def send_tweets(api, tweets):
    ''' Upload multiple tweets'''
    id_ = None  # for first tweet
    for tweet in tweets:
        status = api.update_status(tweet, in_reply_to_status_id=id_)
        id_ = status.id


if __name__ == '__main__':
    chap_verse = gt.get_chap_verse()
    access_token = gt.get_access_token()
    response_eng = gt.get_data(access_token, chap_verse)
    response_hi = gt.get_data(access_token, chap_verse, language='hi')
    text = gt.get_text(response_eng)
    meaning_eng = gt.get_meaning(response_eng)
    meaning_hi = gt.get_meaning(response_hi)
    api = authenticate()
    tweets = []
    tweets = format_tweets(tweets, text)
    tweets = format_tweets(tweets, meaning_eng)
    tweets = format_tweets(tweets, meaning_hi)
    send_tweets(api, tweets)
