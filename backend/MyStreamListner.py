import tweepy
from utils.config import Config
import datetime

conf = Config()
twitter_conf = conf.get_property("twitter")
consumer_key = twitter_conf["consumer_key"]
consumer_secret = twitter_conf["consumer_secret"]
access_token = twitter_conf["access_token"]
access_token_secret = twitter_conf["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    """
    override tweepy.StreamListener to add logic to on_status
    """

    def on_status(self, status):
        if ('RT @' not in status.text):
            tweet_entity = {
                'id_str': status.id_str,
                'text': status.text,
                'username': status.user.screen_name,
                'name': status.user.name,
                'profile_image_url': status.user.profile_image_url,
                'received_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            print(tweet_entity)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['python', 'scala'])


# twitter stream listner and track the words
