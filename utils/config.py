import yaml
class Config:
    def __init__(self):
        with open("../config/config.yaml") as f:
            self.conf = yaml.full_load(f)

    def get_property(self, key):
        confKeys = key.split(".", maxsplit=1)
        if len(confKeys) == 1:
            return self.conf.get(key)
        else:
            return self.conf.get(confKeys[0])[confKeys[1]]


# How to read config.yaml keys
# Option - 01
# c = Config()
# redis_conf = c.get_property("twitter")
# authKey = redis_conf["consumer_key"]

# Option - 02
# print(c.get_property("twitter.consumer_key"))