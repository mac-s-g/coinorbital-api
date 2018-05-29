import json
import sys
from urllib.parse import unquote
sys.path.insert(0, './../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def delete(event, context):

    if "investment" in event['pathParameters']:
        name = unquote(event['pathParameters']['investment'])
    else:
        raise Exception("investment name not valid")

    user = User(event)
    user.deleteInvestment(name)

    user.save()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "success": True,
                "investments": user.investments
            },
            cls=DecimalEncoder
        )
    }
