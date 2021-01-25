from utils.dynamodb_utils import scan_tweets_table_with_pagination, scan_tweets_table_without_pagination
from utils.s3_utils import save_last_evaluated_key_to_json

def print_filter_results(filtered_tweets):
  print("count:", filtered_tweets["count"])
  print("last_evaluated_key:", filtered_tweets["last_evaluated_key"]["id_str"])
  print("scanned_count:", filtered_tweets["scanned_count"])

def filter_from_the_start():
  filtered_tweets = scan_tweets_table_without_pagination()


  save_last_evaluated_key_to_json(filtered_tweets["last_evaluated_key"])

  print_filter_results(filtered_tweets)

  return filtered_tweets

def filter_by_last_evaluated_key(last_evaluated_key):
  filtered_tweets = scan_tweets_table_with_pagination(last_evaluated_key)

  save_last_evaluated_key_to_json(filtered_tweets["last_evaluated_key"])

  print_filter_results(filtered_tweets)

  return filtered_tweets