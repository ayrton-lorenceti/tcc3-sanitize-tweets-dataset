import boto3

events = boto3.client('events')

def disable_rule(name = 'TCC3-StateMachine-Rule'):
  events.disable_rule(
    Name=name
  )