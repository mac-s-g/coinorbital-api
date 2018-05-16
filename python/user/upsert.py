import os
import json
import boto3
import sys
sys.path.insert(0, './../')
from user import user
from user import decimalencoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

def upsert(event, context):
    post = json.loads(event['body'])
    post['user_id'] = user.getId(event)

    if "user" not in post:
        raise Exception('user object required in post')

    result = table.get_item(
        Key={
            'user_id': user.getId(event)
        }
    )
    if result:
        user_record = result['Item']
    else:
        user_record = {
            'user_id': user.getId(event)
        }

    for (key, val) in post['user'].items():
        user_record[key] = val

    table.put_item(Item=user_record)

    return {"statusCode": 200, "body": json.dumps({"success": True})}