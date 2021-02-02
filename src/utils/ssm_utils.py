print("antes de importar o boto3 - ssm_utils")
import boto3
print("depois de importar o boto3 - ssm_utils")
client = boto3.client('ssm')

def get_parameters(parameter_name):
  parameters_response = client.get_parameters(
    Names=[parameter_name],
    WithDecryption=False
  )

  return parameters_response["Parameters"][0]["Value"]