import json
import sys
sys.path.insert(0, './../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def put(event, context):
    post = json.loads(event['body'])

    #could use some extra input validation
    if "watchlist" in post:
        watchlist = post["watchlist"]
    else:
        raise Exception("malformatted request")

    user = User(event)
    user.setWatchlist(watchlist)
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