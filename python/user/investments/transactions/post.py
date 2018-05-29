import json
import sys
from urllib.parse import unquote
sys.path.insert(0, './../../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def post(event, context):
    post = json.loads(event['body'])
    user = User(event)

    if "investment" in event['pathParameters']:
        investment_name = unquote(event['pathParameters']['investment'])
    else:
        raise Exception("investment name not valid")

    if "transaction" in post:
        transaction = post["transaction"]
    else:
        raise Exception("transactions object required in post")

    user.addTransaction(investment_name, transaction)
    user.save()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "success": True,
                "transaction": transaction
            },
            cls=DecimalEncoder
        )
    }