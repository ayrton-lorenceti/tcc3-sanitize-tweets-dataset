from utils.ssm_utils import get_parameters

import tweepy

consumer_key = get_parameters("CONSUMER_KEY")
consumer_secret_key = get_parameters("CONSUMER_SECRET_KEY")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
tweet_mode = "extended"

def get_full_text(id_str):
  result = api.get_status(id_str, tweet_mode=tweet_mode)

  return result["full_text"]