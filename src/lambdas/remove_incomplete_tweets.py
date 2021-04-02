from utils.dynamodb_utils import get_scan_params_by_table
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

    scan_params = get_scan_params_by_table("Classified_Tweets")

    tweets = table.scan(
      FilterExpression=scan_params["filter_expression"],
      ExpressionAttributeValues=scan_params["expression_attribute_values"],
      ExpressionAttributeNames=scan_params["expression_attribute_names"]
    )

    return tweets
  except Exception as exception:
    print(exception)