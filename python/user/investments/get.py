import os
import json
import boto3
import sys
sys.path.insert(0, './../')
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
    user_record = result['Item']
    investment = event['pathParameters']['investment']

    if "investments" in user_record and investment in user_record['investments']:
        response = {
            "statusCode": 200,
            "body": json.dumps(
                user_record['investments'][investment],
                cls=decimalencoder.DecimalEncoder
            )
        }
    else:
        raise Exception("investment: {} not found".format(investment))


    return response