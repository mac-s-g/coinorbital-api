import json
import sys
from urllib.parse import unquote
sys.path.insert(0, './../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def delete(event, context):

    if "symbol" in event['pathParameters']:
        symbol = unquote(event['pathParameters']['symbol'])
    else:
        raise Exception("symbol name not valid")

    user = User(event)
    user.deleteFromWatchlist(symbol)
    user.save()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "success": True,
                "watchlist": user.watchlist
            },
            cls=DecimalEncoder
        )
    }
