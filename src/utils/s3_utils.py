import boto3
import json

s3 = boto3.resource("s3")
object = s3.Object("tcc3bucket", "last_evaluated_key.json")

def read_json_from_s3():
  return json.loads(object.get()['Body'].read().decode('utf-8'))["last_evaluated_key"]

def save_last_evaluated_key_to_json(last_evaluated_key, json_filename = "last_evaluated_key"):
  data = {
    "last_evaluated_key": last_evaluated_key
  }

  object.put(
    Body=((json.dumps(data).encode('UTF-8')))
  )

def save_remove_incomplete_tweets_table_scan_results(scan_results, json_filename = "last_evaluated_key"):
  object = s3.Object("tcc3bucket", f'{json_filename}.json')

  data = {
    "remaining_amount_of_tweets_to_scan": scan_results["remaining_amount"],
    "last_evaluated_key": scan_results["last_evaluated_key"]
  }

  object.put(
    Body=((json.dumps(data).encode('UTF-8')))
  )

