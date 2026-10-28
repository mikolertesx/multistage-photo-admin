import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Signs get request.
def handler(event, context):
    params = event.get("queryStringParameters") or {}
    key = (params.get("key") or "").strip()
    bucket = os.environ.get("BUCKET")

    if not params:
        logger.error("Attempted to sign a get with no params.")
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"message": "No params were provided."}),
        }

    if not key:
        logger.error("Get request has no key.")
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
        "get_object",
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=900,
    )
    logger.info(f"Signed get for key: {key}.")
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"url": url}),
    }
