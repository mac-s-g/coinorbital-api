import os
import json
import boto3
import sys
sys.path.insert(0, './../')
from user import user
from user import decimalencoder


dynamodb = boto3.resource('dynamodb')

def get(event, context):
    table = dynamodb.Table(os.environ['USER_TABLE'])
    user_id = user.getId(event)

    result = table.get_item(
        Key={
            'user_id': user_id
        }
    )

    user_record = result['Item']

    if "transactions" in user_record:
        transactions = user_record['transactions']
    else:
        transactions = user.gettransactionsTemplate()

    response = {
        "statusCode": 200,
        "body": json.dumps(transactions, cls=decimalencoder.DecimalEncoder)
    }

    return response