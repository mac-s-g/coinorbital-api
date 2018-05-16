import os
import json
import boto3
import sys
sys.path.insert(0, './../../')
from user import user
from user import decimalencoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

def get(event, context):
    user_id = user.getId(event)

    if "investment" in event['pathParameters']:
        investment_name = event['pathParameters']['investment']
    else:
        raise Exception("investment name not valid")

    result = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    user_record = result['Item']

    investments = user.getInvestments(user_record)

    if investment_name in investments:
        transactions = user.getTransactions(investments[investment_name])
    else:
        raise Exception("investment not found")

    return {
        "statusCode": 200,
        "body": json.dumps(transactions, cls=decimalencoder.DecimalEncoder)
    }
