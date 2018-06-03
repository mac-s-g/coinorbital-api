import json
import sys
from urllib.parse import unquote
sys.path.insert(0, './../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def upsert(event, context):
    post = json.loads(event['body'])

    if "investment" in event['pathParameters']:
        current_name = unquote(event['pathParameters']['investment'])
    else:
        raise Exception("investment name not valid")

    if "investment" in post:
        investment = post["investment"]
        if "name" not in investment:
            investment["name"] = current_name
    else:
        raise Exception("investment object required in post")

    user = User(event)
    if investment["name"] != current_name:
        if investment["name"] not in user.investments:
            user.deleteInvestment(current_name)
        else:
            raise Exception(
                "error: cannot rename investment, '{}' already exists".format(
                    investment["name"]
                )
            )

    user.setInvestment(investment)
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
