import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lists media projects in S3
def handler(event, context):
    bucket = os.environ.get("BUCKET")

    if not bucket:
        logger.error("No bucket is configured.")
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"message": "Server error, please try later."}),
        }

    s3 = boto3.client("s3")

    # Delimiter groups keys at the next "/", so nested objects stay out of Contents.
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix="projects/",
        Delimiter="/",
        MaxKeys=100,
    )

    # An empty bucket omits CommonPrefixes. Treat that as an empty project list.
    # An empty bucket omits CommonPrefixes. Treat that as an empty project list.
    # CommonPrefixes is the folder list. Contents would only return files,
    # and S3 has no real folders.
    prefixes = response.get("CommonPrefixes", [])
    logger.info(f"Listed {len(prefixes)} projects.")

    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({
            "projectList": prefixes
        }, default=str),
    }
