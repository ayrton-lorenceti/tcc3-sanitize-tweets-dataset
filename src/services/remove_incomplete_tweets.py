from utils.dynamodb_utils import get_scan_params_by_table, get_filtered_tweets, scan_table_using_filters
from utils.s3_utils import save_remove_incomplete_tweets_table_scan_results

table_name = "Classified_Tweets"

def remove_incomplete_tweets_from_the_start():
    scan_params = get_scan_params_by_table(table_name)
    scanned_tweets = scan_table_using_filters(scan_params, table_name)
    filtered_tweets = get_filtered_tweets(scanned_tweets)

    scan_results = get_scan_results(filtered_tweets)
    json_filename = "remove_incomplete_tweets_table_scan_results"
    save_remove_incomplete_tweets_table_scan_results(scan_results, json_filename)

    return scan_results

def get_scan_results(filtered_tweets):
  return {
    "remaining_amount": 134 - filtered_tweets["scanned_count"],
    "last_evaluated_key": filtered_tweets["last_evaluated_key"]
  }