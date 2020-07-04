import redis
import json
from utils.config import Config
from backend.TweetDomain import TweetDomain

class RedisStore:
    redis_conf = Config().get_property("redis")

    def __init__(self):
        self.redis_db = redis.Redis(
            host=self.redis_conf["host_name"],
            port=self.redis_conf["port"],
            password=self.redis_conf["password"])

        self.trim_count = 0
        self.num_tweets = 25

    def push(self, data, redisKey="tweets"):
        self.redis_db.lpush(redisKey, json.dumps(data))
        self.trim_count += 1

        if self.trim_count > 100:
            self.redis_db.ltrim(redisKey, 0, self.num_tweets)
            self.trim_count = 0

    def getTweets(self, redisKey="tweets", limit=15):
        tweets = []
        for tweet in self.redis_db.lrange(redisKey, 0, limit - 1):
            tweetJson = json.loads(tweet)
            print(json.dumps(tweetJson, indent=4, sort_keys=True))
            tweets.append(TweetDomain(tweetJson))
        return tweets
