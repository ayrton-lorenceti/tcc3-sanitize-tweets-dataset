import boto3

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

  return {
    "count": tweets["Count"],
    "tweets": get_tweets_from_items(tweets["Items"]),
    "last_evaluated_key": tweets["LastEvaluatedKey"],
    "scanned_count": tweets["ScannedCount"]
  }