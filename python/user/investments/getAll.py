import json
import sys
sys.path.insert(0, './../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def getAll(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps(
            User(event).get()['investments'],
            cls=DecimalEncoder
        )
    }