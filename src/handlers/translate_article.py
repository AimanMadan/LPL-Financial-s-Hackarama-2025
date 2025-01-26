
import json

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
