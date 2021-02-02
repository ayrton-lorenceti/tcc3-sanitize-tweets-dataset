from services.insert_filtered_tweets_service import insert_filtered_tweets

def lambda_handler(event, context):
  tweets = event["tweets"]

  print("aaa")

  try: 
    return insert_filtered_tweets(tweets)
  except Exception as error:
    return error