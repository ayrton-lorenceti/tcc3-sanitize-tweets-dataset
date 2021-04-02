from services.remove_incomplete_tweets import remove_incomplete_tweets_from_the_start
from utils.s3_utils import read_json_from_s3

import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
  try:
    last_evaluated_key = read_json_from_s3()
    
    return last_evaluated_key
  except s3.exceptions.NoSuchKey as exception:
    return remove_incomplete_tweets_from_the_start()
  except Exception as exception:
    print(exception)