import json
import sys
sys.path.insert(0, './../../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def get(event, context):

    user = User(event).get()

    if "investment" in event['pathParameters']:
        investment_name = event['pathParameters']['investment']
    else:
        raise Exception("investment name not valid")

    if investment_name in user['investments']:
        transactions = user['investments'][investment_name]['transactions']
    else:
        raise Exception("investment not found")

    return {
        "statusCode": 200,
        "body": json.dumps(transactions, cls=DecimalEncoder)
    }
