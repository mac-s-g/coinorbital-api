import json
import sys
sys.path.insert(0, './../')
from user.User import User
from user.decimalencoder import DecimalEncoder
from lambda_decorators import cors_headers

@cors_headers
def upsert(event, context):
    post = json.loads(event['body'])
    if "user" not in post:
        raise Exception('user object required in post')

    user = User(event)

    for (key, val) in post['user'].items():
        user.setItem(key, val)

    user.save()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "success": True,
                "user": user.get()
            },
            cls=DecimalEncoder
        )
    }