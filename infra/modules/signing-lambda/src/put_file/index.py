import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Signs put request
def handler(event, context):
    params = event.get("queryStringParameters") or {}
    key = (params.get("key") or "").strip()
    bucket = os.environ.get("BUCKET")

    if not params:
        logger.error("Attempted to sign a put with no params.")
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"message": "No params were provided."}),
        }

    if not key:
        logger.error("Put request has no key.")
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"message": "No key was provided."}),
        }

    if not bucket:
        logger.error("No bucket is configured.")
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"message": "Server error, please try later."}),
        }

    url = boto3.client("s3").generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=900,
    )
    logger.info(f"Signed put for key: {key}.")
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"url": url}),
    }
