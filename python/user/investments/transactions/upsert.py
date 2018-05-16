import json
import time
import os
import boto3
import sys
sys.path.insert(0, './../../')
from user import user

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

def upsert(event, context):
    post = json.loads(event['body'])

    if "investment" in event['pathParameters']:
        investment_name = event['pathParameters']['investment']
    else:
        raise Exception("investment name not valid")

    if "transactions" in post:
        transactions = post["transactions"]
    else:
        raise Exception("transactions object required in post")

    result = table.get_item(
        Key={
            'user_id': user.getId(event)
        }
    )
    user_record = result['Item']

    investments = user.getInvestments(user_record)

    if investment_name not in investments:
        raise Exception("investment ({}) not found".format(investment_name))

    investments[investment_name]['transactions'] = transactions

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