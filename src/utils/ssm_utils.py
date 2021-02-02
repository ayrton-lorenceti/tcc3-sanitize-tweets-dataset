import boto3

client = boto3.client('ssm')

def get_parameters(parameter_name):
  parameters_response = client.get_parameters(
    Names=[parameter_name],
    WithDecryption=False
  )

  return parameters_response["Parameters"][0]["Value"]