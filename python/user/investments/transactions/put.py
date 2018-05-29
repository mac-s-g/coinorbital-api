import json
import sys
from urllib.parse import unquote
sys.path.insert(0, './../../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def put(event, context):
    post = json.loads(event['body'])
    user = User(event)

    if "investment" in event['pathParameters']:
        investment_name = unquote(event['pathParameters']['investment'])
    else:
        raise Exception("investment name not valid")

    if "transactions" in post:
        transactions = post["transactions"]
    else:
        raise Exception("transactions object required in post")

    user.setTransactions(investment_name, transactions)
    user.save()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "success": True,
                "transactions": transactions
            },
            cls=DecimalEncoder
        )
    }
