from utils.s3_utils import save_last_evaluated_key_to_json

import boto3

events = boto3.client('events')
dynamodb = boto3.resource("dynamodb")

filter_expression = "NOT begins_with(#text, :text)"
expression_attribute_values = { ":text": "RT @" }
expression_attribute_names = { "#text": "text" }

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
    Limit=5
  )

  return get_filtered_tweets(tweets)

def scan_tweets_table_with_pagination(last_evaluated_key, table_name = "Tweets"):
  table = dynamodb.Table(table_name)

  tweets = table.scan(
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ExpressionAttributeNames=expression_attribute_names,
    ExclusiveStartKey=last_evaluated_key,
    Limit=10
  )

  if (tweets["LastEvaluatedKey"] is None):
    last_evaluated_key = {
      "id_str": "-1"
    }

    save_last_evaluated_key_to_json(last_evaluated_key)

    events.disable_rule(
      Name='TCC3-StateMachine-Rule'
    )

    return last_evaluated_key

  return get_filtered_tweets(tweets)