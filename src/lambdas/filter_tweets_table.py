from services.filter_tweets_table_service import filter_by_last_evaluated_key, filter_from_the_start
from utils.s3_utils import read_json_from_s3

def lambda_handler(event, context):
  try:
    last_evaluated_key = read_json_from_s3()
    
    return filter_by_last_evaluated_key(last_evaluated_key)
  except:
    return filter_from_the_start()