from utils.tweepy_utils import get_full_text

import boto3

dynamodb = boto3.resource("dynamodb")
teste_table = dynamodb.Table('Teste')

def insert_filtered_tweets(tweets):
  tweets_saved = 0
  total_tweets = len(tweets)

  print("bbb")

  with teste_table.batch_writer() as batch:
    for tweet in tweets:
      full_text = get_full_text(tweet["id_str"])

      batch.put_item(
        Item={ 
          "id_str": tweet["id_str"], 
          "full_text": full_text
        }
      )

      tweets_saved += 1

  return {
    "tweets_saved": tweets_saved,
    "total_tweets": total_tweets
  }