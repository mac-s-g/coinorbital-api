import json
import sys
sys.path.insert(0, './../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def get(event, context):

    user = User(event).get()
    investment = event['pathParameters']['investment']

    if "investments" in user and investment in user['investments']:
        response = {
            "statusCode": 200,
            "body": json.dumps(
                user['investments'][investment],
                cls=DecimalEncoder
            )
        }
    else:
        raise Exception("investment: {} not found".format(investment))


    return response