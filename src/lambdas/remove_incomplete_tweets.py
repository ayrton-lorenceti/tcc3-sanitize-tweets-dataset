from utils.s3_utils import read_json_from_s3
import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
  try:
    last_evaluated_key = read_json_from_s3()
    
    return last_evaluated_key
  except s3.exceptions.NoSuchKey as exception:
    dynamodb = boto3.resource("dynamodb")

    filter_expression = "contains(... https:/t.co/)"

    table = dynamodb.Table("Classified_Tweets")

    tweets = table.scan(
      FilterExpression=filter_expression
    )

    return tweets
  except Exception as exception:
    print(exception)