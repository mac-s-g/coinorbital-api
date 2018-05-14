import json
import time
import logging
import os
import boto3
import sys
sys.path.insert(0, './../')
from user import user

dynamodb = boto3.resource('dynamodb')


def upsert(event, context):
    table = dynamodb.Table(os.environ['USER_TABLE'])
    user_id = user.getId(event)
    post = json.loads(event['body'])
    timestamp = int(time.time())

    #could use some extra input validation
    if "watchlist" in post:
        watchlist = post["watchlist"]
    else:
        raise Exception("malformatted request")

    result = table.update_item(
        Key={
            'user_id': user_id
        },
        ExpressionAttributeValues={
          ':last_modified': timestamp,
          ':watchlist': watchlist
        },
        UpdateExpression='SET last_modified = :last_modified, '
                         'watchlist = :watchlist'
    )

    return {"statusCode": 200, "body": json.dumps({"success": True})}