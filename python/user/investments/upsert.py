import json
import time
import os
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

    if "investment" in event['pathParameters']:
        name = event['pathParameters']['investment']
    else:
        raise Exception("investment name not valid")

    if "investment" in post:
        investment = post["investment"]
        investment['name'] = name
    else:
        raise Exception("investment object required in post")

    user = User(event).get()
    investments = user['investments']

    if name in investments:
        #if investment already exists, update
        for (key, val) in investment.items():
            investments[name][key] = val
    else:
        #create new investment
        investments[name] = investment

    table.update_item(
        Key={
            'user_id': user['user_id']
        },
        ExpressionAttributeValues={
          ':last_modified': int(time.time()),
          ':investments': investments
        },
        UpdateExpression='SET last_modified = :last_modified, '
                         'investments = :investments'
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"success": True})
    }
