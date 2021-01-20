import boto3

s3 = boto3.resource("s3")
object = s3.Object("tcc3bucket", "last_evaluated_key.json")

def read_json_from_s3():
  return object.get()['Body'].read().decode('utf-8')