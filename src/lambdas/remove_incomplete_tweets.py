from services.remove_incomplete_tweets import remove_incomplete_tweets_from_the_start, remove_incomplete_tweets_by_last_evaluated_key
from utils.s3_utils import read_json_from_s3

import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
  try:
    json_filename = "remove_incomplete_tweets_table_scan_results"
    last_scan_results = read_json_from_s3(json_filename)
    
    return remove_incomplete_tweets_by_last_evaluated_key(last_scan_results)
  except s3.exceptions.NoSuchKey as exception:
    return remove_incomplete_tweets_from_the_start()
  except Exception as exception:
    print(exception)