import os
import json
import boto3
import sys
sys.path.insert(0, './../')
from user import user
from user import decimalencoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

def getAll(event, context):

    result = table.get_item(
        Key={
            'user_id': user.getId(event)
        }
    )
    user_record = result['Item']

    investments = user.getInvestments(user_record)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {name:inv for (name, inv) in investments.items()},
            cls=decimalencoder.DecimalEncoder
        )
    }