def lambda_handler(event, context):
  try:
    return {
      "status": 200,
      "message": "Ok."
    }
  except:
    return {
      "status": 500,
      "message": "Internal."
    }