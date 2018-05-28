import json
import sys
sys.path.insert(0, './../')
from User import User
from decimalencoder import decimalencoder
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
                cls=decimalencoder.DecimalEncoder
            )
        }
    else:
        raise Exception("investment: {} not found".format(investment))


    return response