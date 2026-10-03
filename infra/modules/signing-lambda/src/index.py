import os

import boto3


def handler(event, context):
    return boto3.client("s3").generate_presigned_url(
        "put_object",
        Params={"Bucket": os.environ["BUCKET"], "Key": event["key"]},
        ExpiresIn=900,
    )
