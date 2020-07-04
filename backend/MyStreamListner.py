import tweepy
from utils.config import Config
import datetime
from textblob import TextBlob
import json
from backend.RedisStore import RedisStore


conf = Config()
twitter_conf = conf.get_property("twitter")
consumer_key = twitter_conf["consumer_key"]
consumer_secret = twitter_conf["consumer_secret"]
access_token = twitter_conf["access_token"]
access_token_secret = twitter_conf["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
redisStore = RedisStore()

class MyStreamListener(tweepy.StreamListener):
    """
    override tweepy.StreamListener to add logic to on_status
    """

    def on_status(self, tweet):
        if ('RT @' not in tweet.text):
            polarity, subjectivity = self.getSentimentAttr(tweet.text)

            tweet_entity = {
                'id_str': tweet.id_str,
                'text': tweet.text,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'username': tweet.user.screen_name,
                'name': tweet.user.name,
                'tweet_url': f"https://twitter.com/user/status/{tweet.id}",
                'received_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            print(json.dumps(tweet_entity, indent=4))
            redisStore.push(tweet_entity)


    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.

    def getSentimentAttr(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        return polarity, subjectivity


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['spark 3.0', 'airflow', 'data engineer', 'scala', 'python'])
