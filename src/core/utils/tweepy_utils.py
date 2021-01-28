from utils.ssm_utils import get_parameters

import tweepy

consumer_key = get_parameters("CONSUMER_KEY")
consumer_secret_key = get_parameters("CONSUMER_SECRET_KEY")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())