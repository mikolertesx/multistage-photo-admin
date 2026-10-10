import json
import os

import boto3

# Signs get request.
def handler(event, context):
    url = boto3.client("s3").generate_presigned_url(
        "get_object",
        Params={
            "Bucket": os.environ["BUCKET"],
            "Key": event["queryStringParameters"]["key"],
        },
        ExpiresIn=900,
    )
    return {"statusCode": 200, "body": json.dumps({"url": url})}
