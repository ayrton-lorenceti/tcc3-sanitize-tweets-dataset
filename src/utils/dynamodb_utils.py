import boto3
import pprint

from utils.s3_utils import save_last_evaluated_key_to_json

dynamodb = boto3.resource("dynamodb")

def get_tweets_from_items(tweets):
  return [{ "id_str": tweet["id_str"], "full_text": tweet["text"] } for tweet in tweets]

def scan_tweets_table():
  table = dynamodb.Table('Tweets')
  
  filter_expression = "NOT begins_with(#text, :text)"
  expression_attribute_values = { ":text": "RT @" }
  expression_attribute_names = { "#text": "text" }

  tweets = table.scan(
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ExpressionAttributeNames=expression_attribute_names
  )

  save_last_evaluated_key_to_json(tweets["LastEvaluatedKey"]["id_str"])

  filtered_tweets = {
    "count": tweets["Count"],
    "tweets": get_tweets_from_items(tweets["Items"]),
    "last_evaluated_key": tweets["LastEvaluatedKey"],
    "scanned_count": tweets["ScannedCount"]
  }

  pprint("count: {}\nlast_evaluated_key: {}\nscanned_count: {}".format(filtered_tweets["count"], filtered_tweets["last_evaluated_key"], filtered_tweets["scanned_count"]))
  
  return filtered_tweets 