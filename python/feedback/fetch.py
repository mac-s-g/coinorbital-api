import os
import json

import boto3
dynamodb = boto3.resource('dynamodb')


def fetch(event, context):
    table = dynamodb.Table(os.environ['FEEDBACK_TABLE'])

    body = {
        "payload": table.scan(),
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response