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

    if "investment" in post and "name" in post["investment"]:
        investment = post["investment"]
    else:
        raise Exception("investment.name required in post body")

    result = table.get_item(
        Key={
            'user_id': user.getId(event)
        }
    )
    user_record = result['Item']

    investments = user.getInvestments(user_record)
    investments[investment['name']] = investment

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
