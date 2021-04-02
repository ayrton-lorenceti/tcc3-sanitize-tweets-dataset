from tweepy import TweepError

from utils.events_utils import disable_rule
from utils.s3_utils import save_last_evaluated_key_to_json
from utils.tweepy_utils import get_full_text

import boto3

dynamodb = boto3.resource("dynamodb")

def get_filtered_tweets(tweets):
  filtered_tweets = {
    "count": tweets["Count"],
    "tweets": get_tweets_from_items(tweets["Items"]),
    "last_evaluated_key": tweets["LastEvaluatedKey"],
    "scanned_count": tweets["ScannedCount"]
  }

  return filtered_tweets

def get_scan_params_by_table(last_evaluated_key = None, table_name = "Tweets"):
  if (table_name == "Classified_Tweets"):
    return {
      "filter_expression": "contains(#text, :text)",
      "expression_attribute_values": { ":text": "… https://t.co/" },
      "expression_attribute_names": { "#text": "text" },
      "last_evaluated_key": last_evaluated_key
    }

  return {
    "filter_expression": "NOT begins_with(#text, :text)",
    "expression_attribute_values": { ":text": "RT @" },
    "expression_attribute_names": { "#text": "text" },
    "limit": 100
  }

def get_tweets_from_items(tweets):
  return [{ "id_str": tweet["id_str"], "text": tweet["text"] } for tweet in tweets]

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

def scan_table_using_filters(scan_params, table_name = "Tweets"):
  table = dynamodb.Table(table_name)

  scan_params = get_scan_params_by_table("Classified_Tweets")

  return table.scan(
    FilterExpression=scan_params["filter_expression"],
    ExpressionAttributeValues=scan_params["expression_attribute_values"],
    ExpressionAttributeNames=scan_params["expression_attribute_names"],
    Limit=10
  )

def scan_table_using_filters_by_last_evaluated_key(scan_params, table_name = "Tweets"):
  table = dynamodb.Table(table_name)

  scan_params = get_scan_params_by_table("Classified_Tweets")

  return table.scan(
    FilterExpression=scan_params["filter_expression"],
    ExpressionAttributeValues=scan_params["expression_attribute_values"],
    ExpressionAttributeNames=scan_params["expression_attribute_names"],
    ExclusiveStartKey=scan_params["last_evaluated_key"],
    Limit=10
  )

def scan_tweets_table_with_pagination(last_evaluated_key, table_name = "Tweets"):
  table = dynamodb.Table(table_name)

  scan_params = get_scan_params_by_table()

  tweets = table.scan(
    FilterExpression=scan_params["filter_expression"],
    ExpressionAttributeValues=scan_params["expression_attribute_values"],
    ExpressionAttributeNames=scan_params["expression_attribute_names"],
    ExclusiveStartKey=last_evaluated_key,
    Limit=scan_params["limit"]
  )

  if (tweets["LastEvaluatedKey"] is None):
    last_evaluated_key = {
      "id_str": "-1"
    }

    save_last_evaluated_key_to_json(last_evaluated_key)

    disable_rule()

    return last_evaluated_key

  return get_filtered_tweets(tweets)

def scan_tweets_table_without_pagination(table_name = "Tweets"):
  table = dynamodb.Table(table_name)

  scan_params = get_scan_params_by_table()

  tweets = table.scan(
    FilterExpression=scan_params["filter_expression"],
    ExpressionAttributeValues=scan_params["expression_attribute_values"],
    ExpressionAttributeNames=scan_params["expression_attribute_names"],
    Limit=scan_params["limit"]
  )

  return get_filtered_tweets(tweets)