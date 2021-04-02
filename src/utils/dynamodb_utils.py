from tweepy import TweepError

from utils.events_utils import disable_rule
from utils.s3_utils import save_last_evaluated_key_to_json
from utils.tweepy_utils import get_full_text

import boto3

dynamodb = boto3.resource("dynamodb")

filter_expression = "NOT begins_with(#text, :text)"
expression_attribute_values = { ":text": "RT @" }
expression_attribute_names = { "#text": "text" }
limit = 100

def get_scan_params_by_table(table_name = "Tweets"):
  if (table_name == "Classified_Tweets"):
    return {
      filter_expression: "contains(#text, :text)",
      expression_attribute_values: { ":text": "… https://t.co/" },
      expression_attribute_names: { "#text": "text" }
    }

def get_tweets_from_items(tweets):
  return [{ "id_str": tweet["id_str"], "text": tweet["text"] } for tweet in tweets]

def get_filtered_tweets(tweets):
  filtered_tweets = {
    "count": tweets["Count"],
    "tweets": get_tweets_from_items(tweets["Items"]),
    "last_evaluated_key": tweets["LastEvaluatedKey"],
    "scanned_count": tweets["ScannedCount"]
  }

  return filtered_tweets

def scan_tweets_table_without_pagination(table_name = "Tweets"):
  table = dynamodb.Table(table_name)

  tweets = table.scan(
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ExpressionAttributeNames=expression_attribute_names,
    Limit=limit
  )

  return get_filtered_tweets(tweets)

def scan_tweets_table_with_pagination(last_evaluated_key, table_name = "Tweets"):
  table = dynamodb.Table(table_name)

  tweets = table.scan(
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ExpressionAttributeNames=expression_attribute_names,
    ExclusiveStartKey=last_evaluated_key,
    Limit=limit
  )

  if (tweets["LastEvaluatedKey"] is None):
    last_evaluated_key = {
      "id_str": "-1"
    }

    save_last_evaluated_key_to_json(last_evaluated_key)

    disable_rule()

    return last_evaluated_key

  return get_filtered_tweets(tweets)

def insert_filtered_tweets(tweets, table_name = "Filtered_Tweets"):
  table = dynamodb.Table(table_name)

  tweets_saved = 0
  total_tweets_received = len(tweets)

  with table.batch_writer() as batch:
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
