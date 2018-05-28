import json
import time
import os
import boto3
import sys
sys.path.insert(0, './../../')
from user.User import User
from lambda_decorators import cors_headers

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

@cors_headers
def upsert(event, context):
    post = json.loads(event['body'])
    user = User(event)

    if "investment" in event['pathParameters']:
        investment_name = event['pathParameters']['investment']
    else:
        raise Exception("investment name not valid")

    if "transactions" in post:
        transactions = post["transactions"]
    else:
        raise Exception("transactions object required in post")

    for tx in transactions:
        if user.validTransaction(tx) is False:
            raise Exception("invalid transaction: {}".format(json.dumps(tx)))

    user = User(event).get()

    if investment_name not in user['investments']:
        raise Exception("investment ({}) not found".format(investment_name))

    user['investments'][investment_name]['transactions'] = transactions

    table.update_item(
        Key={
            'user_id': user['user_id']
        },
        ExpressionAttributeValues={
          ':last_modified': int(time.time()),
          ':investments': user['investments']
        },
        UpdateExpression='SET last_modified = :last_modified, '
                         'investments = :investments'
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"success": True})
    }