import json
import time
import logging
import os
import boto3
import sys
sys.path.insert(0, './../')
from User import User
from lambda_decorators import cors_headers

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

@cors_headers
def upsert(event, context):
    post = json.loads(event['body'])

    #could use some extra input validation
    if "watchlist" in post:
        watchlist = post["watchlist"]
    else:
        raise Exception("malformatted request")

    table.update_item(
        Key={
            'user_id': User(event).get().user_id
        },
        ExpressionAttributeValues={
          ':last_modified': int(time.time()),
          ':watchlist': watchlist
        },
        UpdateExpression='SET last_modified = :last_modified, '
                         'watchlist = :watchlist'
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"success": True})
    }