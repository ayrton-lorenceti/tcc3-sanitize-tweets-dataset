from utils.dynamodb_utils import get_scan_params_by_table, get_filtered_tweets
from utils.s3_utils import read_json_from_s3, save_remove_incomplete_tweets_table_scan_results

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

    scanned_tweets = table.scan(
      FilterExpression=scan_params["filter_expression"],
      ExpressionAttributeValues=scan_params["expression_attribute_values"],
      ExpressionAttributeNames=scan_params["expression_attribute_names"],
      Limit=10
    )

    filtered_tweets = get_filtered_tweets(scanned_tweets)

    scan_results = {
      "remaining_amount": 134 - filtered_tweets["scanned_count"],
      "last_evaluated_key": filtered_tweets["last_evaluated_key"]
    }

    json_filename = "remove_incomplete_tweets_table_scan_results"

    save_remove_incomplete_tweets_table_scan_results(scan_results, json_filename)

    return filtered_tweets
  except Exception as exception:
    print(exception)