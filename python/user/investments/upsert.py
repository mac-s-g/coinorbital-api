import json
import time
import os
import boto3
import sys
sys.path.insert(0, './../')
from user import user

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

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

    result = table.get_item(
        Key={
            'user_id': user.getId(event)
        }
    )
    user_record = result['Item']

    investments = user.getInvestments(user_record)

    if name in investments:
        #if investment already exists, update
        for (key, val) in investment.items():
            investments[name][key] = val
    else:
        #create new investment
        investments[name] = investment

    table.update_item(
        Key={
            'user_id': user.getId(event)
        },
        ExpressionAttributeValues={
          ':last_modified': int(time.time()),
          ':investments': investments
        },
        UpdateExpression='SET last_modified = :last_modified, '
                         'investments = :investments'
    )

    return {"statusCode": 200, "body": json.dumps({"success": True})}
