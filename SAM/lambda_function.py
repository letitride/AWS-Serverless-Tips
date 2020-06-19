import boto3
import json
import os

print('Loading function')
dynamo = boto3.resource('dynamodb')

def respond(err, res=None):
  return {
    'statusCode': '400' if err else '200',
    'body': err.message if err else json.dumps(res),
    'headers': {
      'Content-Type': 'application/json'
    }
  }

def lambda_handler(event, context):
  tablename = os.getenv('TABLE_NAME')
  operations = {
    'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
    'GET': lambda dynamo, x: dynamo.scan(),
    'PUT': lambda dynamo, x: dynamo.update_item(**x)
  }

  operation = event['httpMethod']
  if operation in operations:
    payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['bodu'])
    return respond(None, operations[operation](dynamo.Table( tablename ), payload))
  else:
    return respond(ValueError('Unsupported method "{}"'.format(operation)))
