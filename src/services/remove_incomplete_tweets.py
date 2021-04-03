from utils.dynamodb_utils import delete_incomplete_tweets, get_scan_params_by_table, scan_table_using_filters, scan_table_using_filters_by_last_evaluated_key
from utils.s3_utils import save_scan_results
from utils.events_utils import disable_rule

json_filename = "remove_incomplete_tweets_table_scan_results"
table_name = "Filtered_Tweets"

def get_filtered_tweets(tweets):
  filtered_tweets = {
    "count": tweets["Count"],
    "tweets": get_tweets_from_items(tweets["Items"]),
    "last_evaluated_key": tweets["LastEvaluatedKey"],
    "scanned_count": tweets["ScannedCount"]
  }

  return filtered_tweets

def get_tweets_from_items(tweets):
  return [{ "id_str": tweet["id_str"], "text": tweet["full_text"] } for tweet in tweets]

def remove_incomplete_tweets_from_the_start():
    scan_params = get_scan_params_by_table(table_name)
    scanned_tweets = scan_table_using_filters(scan_params, table_name = table_name)
    filtered_tweets = get_filtered_tweets(scanned_tweets)

    delete_incomplete_tweets(filtered_tweets["tweets"], table_name)

    scan_results = get_scan_results(filtered_tweets)
    save_scan_results(scan_results, json_filename)

    return scan_results

def remove_incomplete_tweets_by_last_evaluated_key(last_scan_results):
  scan_params = get_scan_params_by_table(last_scan_results["last_evaluated_key"], table_name)
  scanned_tweets = scan_table_using_filters_by_last_evaluated_key(scan_params, table_name)

  if("LastEvaluatedKey" in scanned_tweets):
    filtered_tweets = get_filtered_tweets(scanned_tweets)

    delete_incomplete_tweets(filtered_tweets["tweets"], table_name)

    scan_results = get_scan_results(filtered_tweets, last_scan_results["remaining_amount_of_tweets_to_scan"])
    save_scan_results(scan_results, json_filename)

    return scan_results
  
  last_remaining_amount = last_scan_results["remaining_amount_of_tweets_to_scan"]
  scan_results = {
    "remaining_amount": last_remaining_amount - scanned_tweets["ScannedCount"],
    "last_evaluated_key": { "id_str": "-1" }
  }
  save_scan_results(scan_results, json_filename)

  rule_name = "remove-incomplete-tweets-rule"
  disable_rule(rule_name)

  return scan_results

def get_scan_results(filtered_tweets, last_remaining_amount = 192924):
  return {
    "remaining_amount": last_remaining_amount - filtered_tweets["scanned_count"],
    "last_evaluated_key": filtered_tweets["last_evaluated_key"]
  }