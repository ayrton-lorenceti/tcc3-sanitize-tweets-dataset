from utils.s3_utils import read_json_from_s3
import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
  try:
    last_evaluated_key = read_json_from_s3()
    
    return last_evaluated_key
  except s3.exceptions.NoSuchKey as exception:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Classified_Tweets")

    filter_expression = "contains(#text, :text)"
    expression_attribute_values = { ":text": "… https://t.co/" }
    expression_attribute_names = { "#text": "text" }

    tweets = table.scan(
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ExpressionAttributeNames=expression_attribute_names,
    )

    return tweets
  except Exception as exception:
    print(exception)