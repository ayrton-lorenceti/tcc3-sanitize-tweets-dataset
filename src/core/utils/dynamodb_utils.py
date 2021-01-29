import boto3

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
    ExpressionAttributeNames=expression_attribute_names
  )

  return get_filtered_tweets(tweets)

def scan_tweets_table_with_pagination(last_evaluated_key, table_name = "Tweets"):
  table = dynamodb.Table(table_name)

  tweets = table.scan(
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ExpressionAttributeNames=expression_attribute_names,
    ExclusiveStartKey=last_evaluated_key
  )

  # if (tweets["LastEvaluatedKey"] is None):
  #   # salva -1 no json
  #   # desabilita lambdas

  return get_filtered_tweets(tweets)