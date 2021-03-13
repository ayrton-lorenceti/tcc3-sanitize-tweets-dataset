import boto3

events = boto3.client('events')

def disable_rule():
  events.disable_rule(
    Name='TCC3-StateMachine-Rule'
  )