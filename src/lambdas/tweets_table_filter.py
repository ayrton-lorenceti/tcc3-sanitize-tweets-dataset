from utils.s3_utils import read_json_from_s3

def lambda_handler(event, context):
  try:
    read_json_from_s3()
    
    return {
      "status": 200,
      "message": "Ok"
    }    
  except Exception as error:
    return error