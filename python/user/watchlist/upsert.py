import json
import time
import logging
import os
import boto3
import sys
sys.path.insert(0, './../')
from user import user

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

def upsert(event, context):
    post = json.loads(event['body'])

    #could use some extra input validation
    if "watchlist" in post:
        watchlist = post["watchlist"]
    else:
        raise Exception("malformatted request")

    table.update_item(
        Key={
            'user_id': user.getId(event)
        },
        ExpressionAttributeValues={
          ':last_modified': int(time.time()),
          ':watchlist': watchlist
        },
        UpdateExpression='SET last_modified = :last_modified, '
                         'watchlist = :watchlist'
    )

    return {"statusCode": 200, "body": json.dumps({"success": True})}