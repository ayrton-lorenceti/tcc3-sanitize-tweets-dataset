from utils.tweepy_utils import get_full_text

from tweepy import TweepError

import boto3

dynamodb = boto3.resource("dynamodb")
teste_table = dynamodb.Table('Teste')

def insert_filtered_tweets(tweets):
  tweets_saved = 0
  total_tweets_received = len(tweets)

  with teste_table.batch_writer() as batch:
    for tweet in tweets:
      try:
        full_text = get_full_text(tweet["id_str"])
        
        batch.put_item(
          Item={ 
            "id_str": tweet["id_str"], 
            "full_text": full_text
          }
        )
      except TweepError as exception:
        print("Error: ", exception)
        
        batch.put_item(
          Item={ 
            "id_str": tweet["id_str"], 
            "full_text": tweet["text"]
          }
        )
      except Exception as exception:
        print("Generic error: ", exception)

        raise Exception(exception)
      finally:
        tweets_saved += 1

  return {
    "tweets_saved": tweets_saved,
    "total_tweets_received": total_tweets_received
  }