from services.insert_filtered_tweets_service import insert_filtered_tweets

def lambda_handler(event, context):
  tweets = event["tweets"]


  return insert_filtered_tweets(tweets)