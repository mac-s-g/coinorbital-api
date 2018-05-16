import os
import json
import boto3
import sys
sys.path.insert(0, './')
from user import user
from user import decimalencoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

def get(event, context):

    result = table.get_item(
        Key={
            'user_id': user.getId(event)
        }
    )

    try:
        user_record = result['Item']
    except:
        user_record = {
            'user_id': user.getId(event)
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(user_record, cls=decimalencoder.DecimalEncoder)
    }

    return response