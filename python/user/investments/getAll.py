import json
import sys
sys.path.insert(0, './../')
from User import User
from decimalencoder import decimalencoder
from lambda_decorators import cors_headers

@cors_headers
def getAll(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps(
            User(event).investments,
            cls=decimalencoder.DecimalEncoder
        )
    }