import tweepy
from utils.config import Config

conf = Config()
twitter_conf = conf.get_property("twitter")
consumer_key = twitter_conf["consumer_key"]
consumer_secret = twitter_conf["consumer_secret"]
access_token = twitter_conf["access_token"]
access_token_secret = twitter_conf["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

