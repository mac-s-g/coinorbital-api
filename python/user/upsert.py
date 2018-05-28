import os
import json
import boto3
import sys
sys.path.insert(0, './../')
from user.User import User
from lambda_decorators import cors_headers

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

@cors_headers
def upsert(event, context):
    post = json.loads(event['body'])
    if "user" not in post:
        raise Exception('user object required in post')

    user = User(event).get()

    for (key, val) in post['user'].items():
        user[key] = val

    table.put_item(Item=user)

    return {
        "statusCode": 200,
        "body": json.dumps({"success": True})
    }