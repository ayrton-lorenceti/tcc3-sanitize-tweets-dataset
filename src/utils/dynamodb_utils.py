import boto3

dynamodb = boto3.resource("dynamodb")

def parse_urls_set_from_tweet_to_list(scanned_tweet):
  scanned_tweet["urls"] = list(scanned_tweet["urls"])
  
  return scanned_tweet

def parse_tweets_urls(scanned_tweets):
  return [
    parse_urls_set_from_tweet_to_list(scanned_tweet) for scanned_tweet in scanned_tweets 
    if len(scanned_tweet["urls"]) > 0
  ]

def scan_tweets_table():
  table = dynamodb.Table('Tweets')
  
  filter_expression = "NOT begins_with(#text, :text)"
  expression_attribute_values = { ":text": "RT @" }
  expression_attribute_names = { "#text": "text" }

  scanned_tweets = table.scan(
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ExpressionAttributeNames=expression_attribute_names
  )

  return {
    "count": scanned_tweets["Count"],
    "items": parse_tweets_urls(scanned_tweets["Items"]),
    "last_evaluated_key": scanned_tweets["LastEvaluatedKey"],
    "scanned_count": scanned_tweets["ScannedCount"]
  }